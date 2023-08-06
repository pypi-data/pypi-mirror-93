# Copyright (c) 2016 Mirantis, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Container Driver for shares.

This driver uses a container as a share server.
Current implementation suggests that a container when started by Docker will
be plugged into a Linux bridge. Also it is suggested that all interfaces
willing to talk to each other reside in an OVS bridge."""

import math
import re

from oslo_config import cfg
from oslo_log import log
from oslo_utils import importutils

from manila import exception
from manila.i18n import _
from manila.share import driver
from manila import utils


CONF = cfg.CONF
LOG = log.getLogger(__name__)


container_opts = [
    cfg.StrOpt("container_linux_bridge_name",
               default="docker0",
               required=True,
               help="Linux bridge used by container hypervisor to plug "
                    "host-side veth to. It will be unplugged from here "
                    "by the driver."),
    cfg.StrOpt("container_ovs_bridge_name",
               default="br-int",
               required=True,
               help="OVS bridge to use to plug a container to."),
    cfg.BoolOpt("container_cifs_guest_ok",
                default=True,
                help="Determines whether to allow guest access to CIFS share "
                     "or not."),
    cfg.StrOpt("container_image_name",
               default="manila-docker-container",
               help="Image to be used for a container-based share server."),
    cfg.StrOpt("container_helper",
               default="manila.share.drivers.container.container_helper."
               "DockerExecHelper",
               help="Container helper which provides container-related "
                    "operations to the driver."),
    cfg.StrOpt("container_protocol_helper",
               default="manila.share.drivers.container.protocol_helper."
               "DockerCIFSHelper",
               help="Helper which facilitates interaction with share server."),
    cfg.StrOpt("container_storage_helper",
               default="manila.share.drivers.container.storage_helper."
               "LVMHelper",
               help="Helper which facilitates interaction with storage "
                    "solution used to actually store data. By default LVM "
                    "is used to provide storage for a share."),
    cfg.StrOpt("container_volume_mount_path",
               default="/tmp/shares",
               help="Folder name in host to which logical volume will be "
                    "mounted prior to providing access to it from a "
                    "container."),
]


class ContainerShareDriver(driver.ShareDriver, driver.ExecuteMixin):
    def __init__(self, *args, **kwargs):
        super(ContainerShareDriver, self).__init__([True], *args, **kwargs)
        self.configuration.append_config_values(container_opts)
        self.backend_name = self.configuration.safe_get(
            "share_backend_name") or "Docker"
        self.container = importutils.import_class(
            self.configuration.container_helper)(
                configuration=self.configuration)
        self.storage = importutils.import_class(
            self.configuration.container_storage_helper)(
                configuration=self.configuration)
        self._helpers = {}

    def _get_helper(self, share):
        if share["share_proto"].upper() == "CIFS":
            helper = self._helpers.get("CIFS")
            if helper is not None:
                return helper(self.container,
                              share=share,
                              config=self.configuration)
            self._helpers["CIFS"] = importutils.import_class(
                self.configuration.container_protocol_helper)
            return self._helpers["CIFS"](self.container,
                                         share=share,
                                         config=self.configuration)
        else:
            raise exception.InvalidShare(
                reason=_("Wrong, unsupported or disabled protocol."))

    def _update_share_stats(self):
        data = {
            'share_backend_name': self.backend_name,
            'storage_protocol': 'CIFS',
            'reserved_percentage':
                self.configuration.reserved_share_percentage,
            'consistency_group_support': None,
            'snapshot_support': False,
            'create_share_from_snapshot_support': False,
            'driver_name': 'ContainerShareDriver',
            'pools': self.storage.get_share_server_pools()
        }
        super(ContainerShareDriver, self)._update_share_stats(data)

    def create_share(self, context, share, share_server=None):
        LOG.debug("Create share on server '%s'.", share_server["id"])
        server_id = self._get_container_name(share_server["id"])
        share_name = share.share_id
        self.storage.provide_storage(share_name, share['size'])

        location = self._create_export_and_mount_storage(
            share, server_id, share_name)

        return location

    @utils.synchronized('container_driver_delete_share_lock', external=True)
    def delete_share(self, context, share, share_server=None):
        LOG.debug("Deleting share %(share)s on server '%(server)s'.",
                  {"server": share_server["id"],
                   "share": self._get_share_name(share)})
        server_id = self._get_container_name(share_server["id"])
        share_name = self._get_share_name(share)

        self._delete_export_and_umount_storage(share, server_id, share_name,
                                               ignore_errors=True)

        self.storage.remove_storage(share_name)
        LOG.debug("Deleted share %s successfully.", share_name)

    def _get_share_name(self, share):
        if share.get('export_location'):
            return share['export_location'].split('/')[-1]
        else:
            return share.share_id

    def extend_share(self, share, new_size, share_server=None):
        server_id = self._get_container_name(share_server["id"])
        share_name = self._get_share_name(share)
        self.container.execute(
            server_id,
            ["umount", "/shares/%s" % share_name]
        )
        self.storage.extend_share(share_name, new_size, share_server)
        lv_device = self.storage._get_lv_device(share_name)
        self.container.execute(
            server_id,
            ["mount", lv_device, "/shares/%s" % share_name]
        )

    def ensure_share(self, context, share, share_server=None):
        pass

    def update_access(self, context, share, access_rules, add_rules,
                      delete_rules, share_server=None):
        server_id = self._get_container_name(share_server["id"])
        share_name = self._get_share_name(share)
        LOG.debug("Updating access to share %(share)s at "
                  "share server %(share_server)s.",
                  {"share_server": share_server["id"],
                   "share": share_name})
        self._get_helper(share).update_access(server_id, share_name,
                                              access_rules, add_rules,
                                              delete_rules)

    def get_network_allocations_number(self):
        return 1

    def _get_container_name(self, server_id):
        return "manila_%s" % server_id.replace("-", "_")

    def do_setup(self, *args, **kwargs):
        pass

    def check_for_setup_error(self, *args, **kwargs):
        host_id = self.configuration.safe_get("neutron_host_id")
        neutron_class = importutils.import_class(
            'manila.network.neutron.neutron_network_plugin.'
            'NeutronNetworkPlugin'
        )
        actual_class = importutils.import_class(
            self.configuration.safe_get("network_api_class"))
        if host_id is None and issubclass(actual_class, neutron_class):
            msg = _("%s requires neutron_host_id to be "
                    "specified.") % neutron_class
            raise exception.ManilaException(msg)
        elif host_id is None:
            LOG.warning("neutron_host_id is not specified. This driver "
                        "might not work as expected without it.")

    def _connect_to_network(self, server_id, network_info, host_veth):
        LOG.debug("Attempting to connect container to neutron network.")
        network_allocation = network_info['network_allocations'][0]
        port_address = network_allocation.ip_address
        port_mac = network_allocation.mac_address
        port_id = network_allocation.id
        self.container.execute(
            server_id,
            ["ifconfig", "eth0", port_address, "up"]
        )
        self.container.execute(
            server_id,
            ["ip", "link", "set", "dev", "eth0", "address", port_mac]
        )
        msg_helper = {
            'id': server_id, 'veth': host_veth,
            'lb': self.configuration.container_linux_bridge_name,
            'ovsb': self.configuration.container_ovs_bridge_name,
            'ip': port_address,
            'network': network_info['neutron_net_id'],
            'subnet': network_info['neutron_subnet_id'],
        }
        LOG.debug("Container %(id)s veth is %(veth)s.", msg_helper)
        LOG.debug("Removing %(veth)s from %(lb)s.", msg_helper)
        self._execute("brctl", "delif",
                      self.configuration.container_linux_bridge_name,
                      host_veth,
                      run_as_root=True)

        LOG.debug("Plugging %(veth)s into %(ovsb)s.", msg_helper)
        set_if = ['--', 'set', 'interface', host_veth]
        e_mac = set_if + ['external-ids:attached-mac="%s"' % port_mac]
        e_id = set_if + ['external-ids:iface-id="%s"' % port_id]
        e_status = set_if + ['external-ids:iface-status=active']
        e_mcid = set_if + ['external-ids:manila-container=%s' % server_id]
        self._execute("ovs-vsctl", "--", "add-port",
                      self.configuration.container_ovs_bridge_name, host_veth,
                      *(e_mac + e_id + e_status + e_mcid), run_as_root=True)
        LOG.debug("Now container %(id)s should be accessible from network "
                  "%(network)s and subnet %(subnet)s by address %(ip)s.",
                  msg_helper)

    @utils.synchronized("container_driver_teardown_lock", external=True)
    def _teardown_server(self, *args, **kwargs):
        server_id = self._get_container_name(kwargs["server_details"]["id"])
        self.container.stop_container(server_id)
        veth = self.container.find_container_veth(server_id)
        if veth:
            LOG.debug("Deleting veth %s.", veth)
            try:
                self._execute("ovs-vsctl", "--", "del-port",
                              self.configuration.container_ovs_bridge_name,
                              veth, run_as_root=True)
            except exception.ProcessExecutionError as e:
                LOG.warning("Failed to delete port %s: port "
                            "vanished.", veth)
                LOG.error(e)

    def _get_veth_state(self):
        result = self._execute("brctl", "show",
                               self.configuration.container_linux_bridge_name,
                               run_as_root=True)
        veths = re.findall("veth.*\\n", result[0])
        veths = [x.rstrip('\n') for x in veths]
        msg = ("The following veth interfaces are plugged into %s now: " %
               self.configuration.container_linux_bridge_name)
        LOG.debug(msg + ", ".join(veths))
        return veths

    def _get_corresponding_veth(self, before, after):
        result = list(set(after) ^ set(before))
        if len(result) != 1:
            raise exception.ManilaException(_("Multiple veths for container."))
        return result[0]

    @utils.synchronized("veth-lock", external=True)
    def _setup_server(self, network_info, metadata=None):
        msg = "Creating share server '%s'."
        server_id = self._get_container_name(network_info["server_id"])
        LOG.debug(msg, server_id)

        veths_before = self._get_veth_state()
        try:
            self.container.start_container(server_id)
        except Exception as e:
            raise exception.ManilaException(_("Cannot create container: %s") %
                                            e)
        veths_after = self._get_veth_state()

        veth = self._get_corresponding_veth(veths_before, veths_after)
        self._connect_to_network(server_id, network_info, veth)
        LOG.info("Container %s was created.", server_id)
        return {"id": network_info["server_id"]}

    def _delete_export_and_umount_storage(
            self, share, server_id, share_name, ignore_errors=False):

        self._umount_storage(
            share, server_id, share_name, ignore_errors=ignore_errors)

        # (aovchinnikov): bug 1621784 manifests itself here as well as in
        # storage helper. There is a chance that we won't be able to remove
        # this directory, despite the fact that it is not shared anymore and
        # already contains nothing. In such case the driver should not fail
        # share deletion, but issue a warning.
        self.container.execute(
            server_id,
            ["rm", "-fR", "/shares/%s" % share_name],
            ignore_errors=True
        )

    def _umount_storage(
            self, share, server_id, share_name, ignore_errors=False):

        self._get_helper(share).delete_share(server_id, share_name,
                                             ignore_errors=ignore_errors)
        self.container.execute(
            server_id,
            ["umount", "/shares/%s" % share_name],
            ignore_errors=ignore_errors
        )

    def _create_export_and_mount_storage(self, share, server_id, share_name):
        self.container.execute(
            server_id,
            ["mkdir", "-m", "750", "/shares/%s" % share_name]
        )
        return self._mount_storage(share, server_id, share_name)

    def _mount_storage(self, share, server_id, share_name):
        lv_device = self.storage._get_lv_device(share_name)
        self.container.execute(
            server_id,
            ["mount", lv_device, "/shares/%s" % share_name]
        )
        location = self._get_helper(share).create_share(server_id)
        return location

    def manage_existing_with_server(
            self, share, driver_options, share_server=None):
        if not share_server and self.driver_handles_share_servers:
            raise exception.ShareBackendException(
                "A share server object is needed to manage a share in this "
                "driver mode of operation.")
        server_id = self._get_container_name(share_server["id"])
        share_name = self._get_share_name(share)
        size = int(math.ceil(float(self.storage.get_size(share_name))))

        self._delete_export_and_umount_storage(share, server_id, share_name)

        new_share_name = share.share_id
        self.storage.rename_storage(share_name, new_share_name)

        location = self._create_export_and_mount_storage(
            share, server_id, new_share_name)

        result = {'size': size, 'export_locations': [location]}
        LOG.info("Successfully managed share %(share)s, returning %(data)s",
                 {'share': share.id, 'data': result})
        return result

    def unmanage_with_server(self, share, share_server=None):
        pass

    def get_share_server_network_info(
            self, context, share_server, identifier, driver_options):
        name = self._get_correct_container_old_name(identifier)
        return [self.container.fetch_container_address(name, "inet")]

    def manage_server(self, context, share_server, identifier, driver_options):
        new_name = self._get_container_name(share_server['id'])
        old_name = self._get_correct_container_old_name(identifier)
        self.container.rename_container(old_name, new_name)
        return new_name, {'id': share_server['id']}

    def unmanage_server(self, server_details, security_services=None):
        pass

    def _get_correct_container_old_name(self, name):
        # Check if the container with the given name exists, else return
        # the name based on the driver template
        if not self.container.container_exists(name):
            return self._get_container_name(name)
        return name

    def migration_check_compatibility(self, context, source_share,
                                      destination_share, share_server=None,
                                      destination_share_server=None):
        return self.storage.migration_check_compatibility(
            context, source_share, destination_share,
            share_server=share_server,
            destination_share_server=destination_share_server)

    def migration_start(self, context, source_share, destination_share,
                        source_snapshots, snapshot_mappings,
                        share_server=None, destination_share_server=None):
        self.storage.migration_start(
            context, source_share, destination_share,
            source_snapshots, snapshot_mappings,
            share_server=share_server,
            destination_share_server=destination_share_server)

    def migration_continue(self, context, source_share, destination_share,
                           source_snapshots, snapshot_mappings,
                           share_server=None, destination_share_server=None):
        return self.storage.migration_continue(
            context, source_share, destination_share,
            source_snapshots, snapshot_mappings, share_server=share_server,
            destination_share_server=destination_share_server)

    def migration_get_progress(self, context, source_share,
                               destination_share, source_snapshots,
                               snapshot_mappings, share_server=None,
                               destination_share_server=None):
        return self.storage.migration_get_progress(
            context, source_share, destination_share,
            source_snapshots, snapshot_mappings, share_server=share_server,
            destination_share_server=destination_share_server)

    def migration_cancel(self, context, source_share, destination_share,
                         source_snapshots, snapshot_mappings,
                         share_server=None, destination_share_server=None):
        self.storage.migration_cancel(
            context, source_share, destination_share,
            source_snapshots, snapshot_mappings, share_server=share_server,
            destination_share_server=destination_share_server)

    def migration_complete(self, context, source_share, destination_share,
                           source_snapshots, snapshot_mappings,
                           share_server=None, destination_share_server=None):
        # Removes the source share reference from the source container
        source_server_id = self._get_container_name(share_server["id"])
        self._umount_storage(
            source_share, source_server_id, source_share.share_id)

        # storage removes source share
        self.storage.migration_complete(
            context, source_share, destination_share,
            source_snapshots, snapshot_mappings, share_server=share_server,
            destination_share_server=destination_share_server)

        # Enables the access on the destination container
        destination_server_id = self._get_container_name(
            destination_share_server["id"])
        new_export_location = self._mount_storage(
            destination_share, destination_server_id,
            destination_share.share_id)

        msg = ("Volume move operation for share %(shr)s was completed "
               "successfully. Share has been moved from %(src)s to "
               "%(dest)s.")
        msg_args = {
            'shr': source_share['id'],
            'src': source_share['host'],
            'dest': destination_share['host'],
        }
        LOG.info(msg, msg_args)

        return {
            'export_locations': new_export_location,
        }

    def share_server_migration_check_compatibility(
            self, context, share_server, dest_host, old_share_network,
            new_share_network, shares_request_spec):
        """Is called to check migration compatibility for a share server."""
        return self.storage.share_server_migration_check_compatibility(
            context, share_server, dest_host, old_share_network,
            new_share_network, shares_request_spec)

    def share_server_migration_start(self, context, src_share_server,
                                     dest_share_server, shares, snapshots):
        """Is called to perform 1st phase of migration of a share server."""
        LOG.debug(
            "Migration of share server with ID '%s' has been started.",
            src_share_server["id"])
        self.storage.share_server_migration_start(
            context, src_share_server, dest_share_server, shares, snapshots)

    def share_server_migration_continue(self, context, src_share_server,
                                        dest_share_server, shares, snapshots):

        return self.storage.share_server_migration_continue(
            context, src_share_server, dest_share_server, shares, snapshots)

    def share_server_migration_cancel(self, context, src_share_server,
                                      dest_share_server, shares, snapshots):
        """Is called to cancel a share server migration."""
        self.storage.share_server_migration_cancel(
            context, src_share_server, dest_share_server, shares, snapshots)
        LOG.debug(
            "Migration of share server with ID '%s' has been canceled.",
            src_share_server["id"])
        return

    def share_server_migration_get_progress(self, context, src_share_server,
                                            dest_share_server, shares,
                                            snapshots):
        """Is called to get share server migration progress."""
        return self.storage.share_server_migration_get_progress(
            context, src_share_server, dest_share_server, shares, snapshots)

    def share_server_migration_complete(self, context, source_share_server,
                                        dest_share_server, shares, snapshots,
                                        new_network_allocations):
        # Removes the source shares reference from the source container
        source_server_id = self._get_container_name(source_share_server["id"])
        for source_share in shares:
            self._umount_storage(
                source_share, source_server_id, source_share.share_id)

        # storage removes source share
        self.storage.share_server_migration_complete(
            context, source_share_server, dest_share_server, shares, snapshots,
            new_network_allocations)

        destination_server_id = self._get_container_name(
            dest_share_server["id"])
        shares_updates = {}
        for destination_share in shares:
            share_id = destination_share.share_id
            new_export_location = self._mount_storage(
                destination_share, destination_server_id, share_id)

            shares_updates[destination_share['id']] = {
                'export_locations': new_export_location,
                'pool_name': self.storage.get_share_pool_name(share_id),
            }

        msg = ("Volumes move operation from server %(server)s were completed "
               "successfully. Share server has been moved from %(src)s to "
               "%(dest)s.")
        msg_args = {
            'serv': source_share_server['id'],
            'src': source_share_server['host'],
            'dest': dest_share_server['host'],
        }
        LOG.info(msg, msg_args)

        return {
            'share_updates': shares_updates,
        }
