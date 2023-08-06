# Copyright (c) 2015 Clinton Knight.  All rights reserved.
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
"""
NetApp Data ONTAP cDOT multi-SVM storage driver library.

This library extends the abstract base library and completes the multi-SVM
functionality needed by the cDOT multi-SVM Manila driver.  This library
variant creates Data ONTAP storage virtual machines (i.e. 'vservers')
as needed to provision shares.
"""

import re

from oslo_log import log
from oslo_serialization import jsonutils
from oslo_utils import excutils

from manila import exception
from manila.i18n import _
from manila.share.drivers.netapp.dataontap.client import client_cmode
from manila.share.drivers.netapp.dataontap.cluster_mode import data_motion
from manila.share.drivers.netapp.dataontap.cluster_mode import lib_base
from manila.share.drivers.netapp import utils as na_utils
from manila.share import utils as share_utils
from manila import utils

LOG = log.getLogger(__name__)
SUPPORTED_NETWORK_TYPES = (None, 'flat', 'vlan')
SEGMENTED_NETWORK_TYPES = ('vlan',)
DEFAULT_MTU = 1500
CLUSTER_IPSPACES = ('Cluster', 'Default')


class NetAppCmodeMultiSVMFileStorageLibrary(
        lib_base.NetAppCmodeFileStorageLibrary):

    @na_utils.trace
    def check_for_setup_error(self):

        if self._have_cluster_creds:
            if self.configuration.netapp_vserver:
                msg = ('Vserver is specified in the configuration. This is '
                       'ignored when the driver is managing share servers.')
                LOG.warning(msg)

        else:  # only have vserver creds, which is an error in multi_svm mode
            msg = _('Cluster credentials must be specified in the '
                    'configuration when the driver is managing share servers.')
            raise exception.InvalidInput(reason=msg)

        # Ensure one or more aggregates are available.
        if not self._find_matching_aggregates():
            msg = _('No aggregates are available for provisioning shares. '
                    'Ensure that the configuration option '
                    'netapp_aggregate_name_search_pattern is set correctly.')
            raise exception.NetAppException(msg)

        (super(NetAppCmodeMultiSVMFileStorageLibrary, self).
            check_for_setup_error())

    @na_utils.trace
    def _get_vserver(self, share_server=None, vserver_name=None):

        if share_server:
            backend_details = share_server.get('backend_details')
            vserver = backend_details.get(
                'vserver_name') if backend_details else None

            if not vserver:
                msg = _('Vserver name is absent in backend details. Please '
                        'check whether Vserver was created properly.')
                raise exception.VserverNotSpecified(msg)
        elif vserver_name:
            vserver = vserver_name
        else:
            msg = _('Share server not provided')
            raise exception.InvalidInput(reason=msg)

        if not self._client.vserver_exists(vserver):
            raise exception.VserverNotFound(vserver=vserver)

        vserver_client = self._get_api_client(vserver)
        return vserver, vserver_client

    def _get_ems_pool_info(self):
        return {
            'pools': {
                'vserver': None,
                'aggregates': self._find_matching_aggregates(),
            },
        }

    @na_utils.trace
    def _handle_housekeeping_tasks(self):
        """Handle various cleanup activities."""
        self._client.prune_deleted_nfs_export_policies()
        self._client.prune_deleted_snapshots()
        self._client.remove_unused_qos_policy_groups()

        (super(NetAppCmodeMultiSVMFileStorageLibrary, self).
            _handle_housekeeping_tasks())

    @na_utils.trace
    def _find_matching_aggregates(self):
        """Find all aggregates match pattern."""
        aggregate_names = self._client.list_non_root_aggregates()
        pattern = self.configuration.netapp_aggregate_name_search_pattern
        return [aggr_name for aggr_name in aggregate_names
                if re.match(pattern, aggr_name)]

    @na_utils.trace
    def setup_server(self, network_info, metadata=None):
        """Creates and configures new Vserver."""

        vlan = network_info['segmentation_id']
        ports = {}
        for network_allocation in network_info['network_allocations']:
            ports[network_allocation['id']] = network_allocation['ip_address']

        @utils.synchronized('netapp-VLAN-%s' % vlan, external=True)
        def setup_server_with_lock():
            LOG.debug('Creating server %s', network_info['server_id'])
            self._validate_network_type(network_info)

            vserver_name = self._get_vserver_name(network_info['server_id'])
            server_details = {
                'vserver_name': vserver_name,
                'ports': jsonutils.dumps(ports)
            }

            try:
                self._create_vserver(vserver_name, network_info)
            except Exception as e:
                e.detail_data = {'server_details': server_details}
                raise

            return server_details

        return setup_server_with_lock()

    @na_utils.trace
    def _validate_network_type(self, network_info):
        """Raises exception if the segmentation type is incorrect."""
        if network_info['network_type'] not in SUPPORTED_NETWORK_TYPES:
            msg = _('The specified network type %s is unsupported by the '
                    'NetApp clustered Data ONTAP driver')
            raise exception.NetworkBadConfigurationException(
                reason=msg % network_info['network_type'])

    @na_utils.trace
    def _get_vserver_name(self, server_id):
        return self.configuration.netapp_vserver_name_template % server_id

    @na_utils.trace
    def _create_vserver(self, vserver_name, network_info):
        """Creates Vserver with given parameters if it doesn't exist."""

        if self._client.vserver_exists(vserver_name):
            msg = _('Vserver %s already exists.')
            raise exception.NetAppException(msg % vserver_name)

        # NOTE(lseki): If there's already an ipspace created for the same VLAN
        # port, reuse it. It will be named after the previously created share
        # server's neutron subnet id.
        node_name = self._client.list_cluster_nodes()[0]
        port = self._get_node_data_port(node_name)
        vlan = network_info['segmentation_id']
        ipspace_name = self._client.get_ipspace_name_for_vlan_port(
            node_name, port, vlan) or self._create_ipspace(network_info)

        LOG.debug('Vserver %s does not exist, creating.', vserver_name)
        self._client.create_vserver(
            vserver_name,
            self.configuration.netapp_root_volume_aggregate,
            self.configuration.netapp_root_volume,
            self._find_matching_aggregates(),
            ipspace_name)

        vserver_client = self._get_api_client(vserver=vserver_name)
        security_services = None
        try:
            self._create_vserver_lifs(vserver_name,
                                      vserver_client,
                                      network_info,
                                      ipspace_name)

            self._create_vserver_admin_lif(vserver_name,
                                           vserver_client,
                                           network_info,
                                           ipspace_name)

            self._create_vserver_routes(vserver_client,
                                        network_info)

            vserver_client.enable_nfs(
                self.configuration.netapp_enabled_share_protocols)

            security_services = network_info.get('security_services')
            if security_services:
                self._client.setup_security_services(security_services,
                                                     vserver_client,
                                                     vserver_name)
        except Exception:
            with excutils.save_and_reraise_exception():
                LOG.error("Failed to configure Vserver.")
                # NOTE(dviroel): At this point, the lock was already acquired
                # by the caller of _create_vserver.
                self._delete_vserver(vserver_name,
                                     security_services=security_services,
                                     needs_lock=False)

    def _get_valid_ipspace_name(self, network_id):
        """Get IPspace name according to network id."""
        return 'ipspace_' + network_id.replace('-', '_')

    @na_utils.trace
    def _create_ipspace(self, network_info):
        """If supported, create an IPspace for a new Vserver."""

        if not self._client.features.IPSPACES:
            return None

        if (network_info['network_allocations'][0]['network_type']
                not in SEGMENTED_NETWORK_TYPES):
            return client_cmode.DEFAULT_IPSPACE

        # NOTE(cknight): Neutron needs cDOT IP spaces because it can provide
        # overlapping IP address ranges for different subnets.  That is not
        # believed to be an issue for any of Manila's other network plugins.
        ipspace_id = network_info.get('neutron_subnet_id')
        if not ipspace_id:
            return client_cmode.DEFAULT_IPSPACE

        ipspace_name = self._get_valid_ipspace_name(ipspace_id)
        self._client.create_ipspace(ipspace_name)

        return ipspace_name

    @na_utils.trace
    def _create_vserver_lifs(self, vserver_name, vserver_client, network_info,
                             ipspace_name):
        """Create Vserver data logical interfaces (LIFs)."""

        nodes = self._client.list_cluster_nodes()
        node_network_info = zip(nodes, network_info['network_allocations'])

        for node_name, network_allocation in node_network_info:
            lif_name = self._get_lif_name(node_name, network_allocation)
            self._create_lif(vserver_client, vserver_name, ipspace_name,
                             node_name, lif_name, network_allocation)

    @na_utils.trace
    def _create_vserver_admin_lif(self, vserver_name, vserver_client,
                                  network_info, ipspace_name):
        """Create Vserver admin LIF, if defined."""

        network_allocations = network_info.get('admin_network_allocations')
        if not network_allocations:
            LOG.info('No admin network defined for Vserver %s.',
                     vserver_name)
            return

        node_name = self._client.list_cluster_nodes()[0]
        network_allocation = network_allocations[0]
        lif_name = self._get_lif_name(node_name, network_allocation)

        self._create_lif(vserver_client, vserver_name, ipspace_name,
                         node_name, lif_name, network_allocation)

    @na_utils.trace
    def _create_vserver_routes(self, vserver_client, network_info):
        """Create Vserver route and set gateways."""
        route_gateways = []
        # NOTE(gouthamr): Use the gateway from the tenant subnet/s
        # for the static routes. Do not configure a route for the admin
        # subnet because fast path routing will work for incoming
        # connections and there are no requirements for outgoing
        # connections on the admin network yet.
        for net_allocation in (network_info['network_allocations']):
            if net_allocation['gateway'] not in route_gateways:
                vserver_client.create_route(net_allocation['gateway'])
                route_gateways.append(net_allocation['gateway'])

    @na_utils.trace
    def _get_node_data_port(self, node):
        port_names = self._client.list_node_data_ports(node)
        pattern = self.configuration.netapp_port_name_search_pattern
        matched_port_names = [port_name for port_name in port_names
                              if re.match(pattern, port_name)]
        if not matched_port_names:
            raise exception.NetAppException(
                _('Could not find eligible network ports on node %s on which '
                  'to create Vserver LIFs.') % node)
        return matched_port_names[0]

    def _get_lif_name(self, node_name, network_allocation):
        """Get LIF name based on template from manila.conf file."""
        lif_name_args = {
            'node': node_name,
            'net_allocation_id': network_allocation['id'],
        }
        return self.configuration.netapp_lif_name_template % lif_name_args

    @na_utils.trace
    def _create_lif(self, vserver_client, vserver_name, ipspace_name,
                    node_name, lif_name, network_allocation):
        """Creates LIF for Vserver."""

        port = self._get_node_data_port(node_name)
        ip_address = network_allocation['ip_address']
        netmask = utils.cidr_to_netmask(network_allocation['cidr'])
        vlan = network_allocation['segmentation_id']
        network_mtu = network_allocation.get('mtu')
        mtu = network_mtu or DEFAULT_MTU

        if not vserver_client.network_interface_exists(
                vserver_name, node_name, port, ip_address, netmask, vlan):

            self._client.create_network_interface(
                ip_address, netmask, vlan, node_name, port, vserver_name,
                lif_name, ipspace_name, mtu)

    @na_utils.trace
    def get_network_allocations_number(self):
        """Get number of network interfaces to be created."""
        return len(self._client.list_cluster_nodes())

    @na_utils.trace
    def get_admin_network_allocations_number(self, admin_network_api):
        """Get number of network allocations for creating admin LIFs."""
        return 1 if admin_network_api else 0

    @na_utils.trace
    def teardown_server(self, server_details, security_services=None):
        """Teardown share server."""
        vserver = server_details.get(
            'vserver_name') if server_details else None

        if not vserver:
            LOG.warning("Vserver not specified for share server being "
                        "deleted. Deletion of share server record will "
                        "proceed anyway.")
            return

        elif not self._client.vserver_exists(vserver):
            LOG.warning("Could not find Vserver for share server being "
                        "deleted: %s. Deletion of share server "
                        "record will proceed anyway.", vserver)
            return

        self._delete_vserver(vserver, security_services=security_services)

    @na_utils.trace
    def _delete_vserver(self, vserver, security_services=None,
                        needs_lock=True):
        """Delete a Vserver plus IPspace and security services as needed."""

        ipspace_name = self._client.get_vserver_ipspace(vserver)

        vserver_client = self._get_api_client(vserver=vserver)
        network_interfaces = vserver_client.get_network_interfaces()

        interfaces_on_vlans = []
        vlans = []
        for interface in network_interfaces:
            if '-' in interface['home-port']:
                interfaces_on_vlans.append(interface)
                vlans.append(interface['home-port'])

        if vlans:
            vlans = '-'.join(sorted(set(vlans))) if vlans else None
            vlan_id = vlans.split('-')[-1]
        else:
            vlan_id = None

        def _delete_vserver_without_lock():
            # NOTE(dviroel): Attempt to delete all vserver peering
            # created by replication
            self._delete_vserver_peers(vserver)

            self._client.delete_vserver(vserver,
                                        vserver_client,
                                        security_services=security_services)

            if (ipspace_name and ipspace_name not in CLUSTER_IPSPACES
                    and not self._client.ipspace_has_data_vservers(
                        ipspace_name)):
                self._client.delete_ipspace(ipspace_name)

            self._delete_vserver_vlans(interfaces_on_vlans)

        @utils.synchronized('netapp-VLAN-%s' % vlan_id, external=True)
        def _delete_vserver_with_lock():
            _delete_vserver_without_lock()

        if needs_lock:
            return _delete_vserver_with_lock()
        else:
            return _delete_vserver_without_lock()

    @na_utils.trace
    def _delete_vserver_vlans(self, network_interfaces_on_vlans):
        """Delete Vserver's VLAN configuration from ports"""
        for interface in network_interfaces_on_vlans:
            try:
                home_port = interface['home-port']
                port, vlan = home_port.split('-')
                node = interface['home-node']
                self._client.delete_vlan(node, port, vlan)
            except exception.NetAppException:
                LOG.exception("Deleting Vserver VLAN failed.")

    @na_utils.trace
    def _delete_vserver_peers(self, vserver):
        vserver_peers = self._get_vserver_peers(vserver=vserver)
        for peer in vserver_peers:
            self._delete_vserver_peer(peer.get('vserver'),
                                      peer.get('peer-vserver'))

    def get_configured_ip_versions(self):
        versions = [4]
        options = self._client.get_net_options()
        if options['ipv6-enabled']:
            versions.append(6)
        return versions

    @na_utils.trace
    def create_replica(self, context, replica_list, new_replica,
                       access_rules, share_snapshots, share_server=None):
        """Creates the new replica on this backend and sets up SnapMirror.

        It creates the peering between the associated vservers before creating
        the share replica and setting up the SnapMirror.
        """
        # 1. Retrieve source and destination vservers from both replicas,
        # active and and new_replica
        src_vserver, dst_vserver = self._get_vservers_from_replicas(
            context, replica_list, new_replica)

        # 2. Retrieve the active replica host's client and cluster name
        src_replica = self.find_active_replica(replica_list)

        src_replica_host = share_utils.extract_host(
            src_replica['host'], level='backend_name')
        src_replica_client = data_motion.get_client_for_backend(
            src_replica_host, vserver_name=src_vserver)
        # Cluster name is needed for setting up the vserver peering
        src_replica_cluster_name = src_replica_client.get_cluster_name()

        # 3. Retrieve new replica host's client
        new_replica_host = share_utils.extract_host(
            new_replica['host'], level='backend_name')
        new_replica_client = data_motion.get_client_for_backend(
            new_replica_host, vserver_name=dst_vserver)
        new_replica_cluster_name = new_replica_client.get_cluster_name()

        if (dst_vserver != src_vserver
                and not self._get_vserver_peers(dst_vserver, src_vserver)):
            # 3.1. Request vserver peer creation from new_replica's host
            # to active replica's host
            new_replica_client.create_vserver_peer(
                dst_vserver, src_vserver,
                peer_cluster_name=src_replica_cluster_name)

            # 3.2. Accepts the vserver peering using active replica host's
            # client (inter-cluster only)
            if new_replica_cluster_name != src_replica_cluster_name:
                src_replica_client.accept_vserver_peer(src_vserver,
                                                       dst_vserver)

        return (super(NetAppCmodeMultiSVMFileStorageLibrary, self).
                create_replica(context, replica_list, new_replica,
                               access_rules, share_snapshots))

    def delete_replica(self, context, replica_list, replica, share_snapshots,
                       share_server=None):
        """Removes the replica on this backend and destroys SnapMirror.

        Removes the replica, destroys the SnapMirror and delete the vserver
        peering if needed.
        """
        vserver, peer_vserver = self._get_vservers_from_replicas(
            context, replica_list, replica)
        super(NetAppCmodeMultiSVMFileStorageLibrary, self).delete_replica(
            context, replica_list, replica, share_snapshots)

        # Check if there are no remaining SnapMirror connections and if a
        # vserver peering exists and delete it.
        snapmirrors = self._get_snapmirrors(vserver, peer_vserver)
        snapmirrors_from_peer = self._get_snapmirrors(peer_vserver, vserver)
        peers = self._get_vserver_peers(peer_vserver, vserver)
        if not (snapmirrors or snapmirrors_from_peer) and peers:
            self._delete_vserver_peer(peer_vserver, vserver)

    def manage_server(self, context, share_server, identifier, driver_options):
        """Manages a vserver by renaming it and returning backend_details."""
        new_vserver_name = self._get_vserver_name(share_server['id'])
        old_vserver_name = self._get_correct_vserver_old_name(identifier)

        if new_vserver_name != old_vserver_name:
            self._client.rename_vserver(old_vserver_name, new_vserver_name)

        backend_details = {'vserver_name': new_vserver_name}
        return new_vserver_name, backend_details

    def unmanage_server(self, server_details, security_services=None):
        pass

    def get_share_server_network_info(
            self, context, share_server, identifier, driver_options):
        """Returns a list of IPs for each vserver network interface."""
        vserver_name = self._get_correct_vserver_old_name(identifier)

        vserver, vserver_client = self._get_vserver(vserver_name=vserver_name)

        interfaces = vserver_client.get_network_interfaces()
        allocations = []
        for lif in interfaces:
            allocations.append(lif['address'])
        return allocations

    def _get_correct_vserver_old_name(self, identifier):

        # In case vserver_name includes the template, we check and add it here
        if not self._client.vserver_exists(identifier):
            return self._get_vserver_name(identifier)
        return identifier

    def _get_snapmirrors(self, vserver, peer_vserver):
        return self._client.get_snapmirrors(
            source_vserver=vserver, source_volume=None,
            destination_vserver=peer_vserver, destination_volume=None)

    def _get_vservers_from_replicas(self, context, replica_list, new_replica):
        active_replica = self.find_active_replica(replica_list)

        dm_session = data_motion.DataMotionSession()
        vserver = dm_session.get_vserver_from_share(active_replica)
        peer_vserver = dm_session.get_vserver_from_share(new_replica)

        return vserver, peer_vserver

    def _get_vserver_peers(self, vserver=None, peer_vserver=None):
        return self._client.get_vserver_peers(vserver, peer_vserver)

    def _create_vserver_peer(self, context, vserver, peer_vserver):
        self._client.create_vserver_peer(vserver, peer_vserver)

    def _delete_vserver_peer(self, vserver, peer_vserver):
        self._client.delete_vserver_peer(vserver, peer_vserver)
