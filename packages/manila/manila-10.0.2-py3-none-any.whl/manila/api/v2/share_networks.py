# Copyright 2014 NetApp
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

"""The shares api."""

import copy
from oslo_db import exception as db_exception
from oslo_log import log
from oslo_utils import timeutils
import six
from six.moves import http_client
import webob
from webob import exc

from manila.api import common
from manila.api.openstack import api_version_request as api_version
from manila.api.openstack import wsgi
from manila.api.views import share_networks as share_networks_views
from manila.db import api as db_api
from manila import exception
from manila.i18n import _
from manila import policy
from manila import quota
from manila.share import rpcapi as share_rpcapi
from manila import utils

RESOURCE_NAME = 'share_network'
RESOURCES_NAME = 'share_networks'
LOG = log.getLogger(__name__)
QUOTAS = quota.QUOTAS


class ShareNetworkController(wsgi.Controller):
    """The Share Network API controller for the OpenStack API."""

    _view_builder_class = share_networks_views.ViewBuilder

    def __init__(self):
        super(ShareNetworkController, self).__init__()
        self.share_rpcapi = share_rpcapi.ShareAPI()

    def show(self, req, id):
        """Return data about the requested network info."""
        context = req.environ['manila.context']
        policy.check_policy(context, RESOURCE_NAME, 'show')

        try:
            share_network = db_api.share_network_get(context, id)
        except exception.ShareNetworkNotFound as e:
            raise exc.HTTPNotFound(explanation=six.text_type(e))

        return self._view_builder.build_share_network(req, share_network)

    def _all_share_servers_are_auto_deletable(self, share_network):
        return all([ss['is_auto_deletable'] for ss
                    in share_network['share_servers']])

    def _share_network_contains_subnets(self, share_network):
        return len(share_network['share_network_subnets']) > 1

    def delete(self, req, id):
        """Delete specified share network."""
        context = req.environ['manila.context']
        policy.check_policy(context, RESOURCE_NAME, 'delete')

        try:
            share_network = db_api.share_network_get(context, id)
        except exception.ShareNetworkNotFound as e:
            raise exc.HTTPNotFound(explanation=six.text_type(e))

        share_instances = (
            db_api.share_instances_get_all_by_share_network(context, id)
        )
        if share_instances:
            msg = _("Can not delete share network %(id)s, it has "
                    "%(len)s share(s).") % {'id': id,
                                            'len': len(share_instances)}
            LOG.error(msg)
            raise exc.HTTPConflict(explanation=msg)

        # NOTE(ameade): Do not allow deletion of share network used by share
        # group
        sg_count = db_api.count_share_groups_in_share_network(context, id)
        if sg_count:
            msg = _("Can not delete share network %(id)s, it has %(len)s "
                    "share group(s).") % {'id': id, 'len': sg_count}
            LOG.error(msg)
            raise exc.HTTPConflict(explanation=msg)

        # NOTE(silvacarlose): Do not allow the deletion of share networks
        # if it still contains two or more subnets
        if self._share_network_contains_subnets(share_network):
            msg = _("The share network %(id)s has more than one subnet "
                    "attached. Please remove the subnets untill you have one "
                    "or no subnets remaining.") % {'id': id}
            LOG.error(msg)
            raise exc.HTTPConflict(explanation=msg)

        for subnet in share_network['share_network_subnets']:
            if not self._all_share_servers_are_auto_deletable(subnet):
                msg = _("The service cannot determine if there are any "
                        "non-managed shares on the share network subnet "
                        "%(id)s, so it cannot be deleted. Please contact the "
                        "cloud administrator to rectify.") % {
                    'id': subnet['id']}
                LOG.error(msg)
                raise exc.HTTPConflict(explanation=msg)

        for subnet in share_network['share_network_subnets']:
            for share_server in subnet['share_servers']:
                self.share_rpcapi.delete_share_server(context, share_server)

        db_api.share_network_delete(context, id)

        try:
            reservations = QUOTAS.reserve(
                context, project_id=share_network['project_id'],
                share_networks=-1, user_id=share_network['user_id'])
        except Exception:
            LOG.exception("Failed to update usages deleting "
                          "share-network.")
        else:
            QUOTAS.commit(context, reservations,
                          project_id=share_network['project_id'],
                          user_id=share_network['user_id'])
        return webob.Response(status_int=http_client.ACCEPTED)

    def _subnet_has_search_opt(self, key, value, network, exact_value=False):
        for subnet in network.get('share_network_subnets') or []:
            if subnet.get(key) == value or (
                    not exact_value and
                    value in subnet.get(key.rstrip('~'))
                    if key.endswith('~') and
                    subnet.get(key.rstrip('~')) else ()):
                return True
        return False

    def _get_share_networks(self, req, is_detail=True):
        """Returns a list of share networks."""
        context = req.environ['manila.context']
        search_opts = {}
        search_opts.update(req.GET)

        if 'security_service_id' in search_opts:
            networks = db_api.share_network_get_all_by_security_service(
                context, search_opts['security_service_id'])
        elif context.is_admin and 'project_id' in search_opts:
            networks = db_api.share_network_get_all_by_project(
                context, search_opts['project_id'])
        elif context.is_admin and utils.is_all_tenants(search_opts):
            networks = db_api.share_network_get_all(context)
        else:
            networks = db_api.share_network_get_all_by_project(
                context,
                context.project_id)

        date_parsing_error_msg = '''%s is not in yyyy-mm-dd format.'''
        if 'created_since' in search_opts:
            try:
                created_since = timeutils.parse_strtime(
                    search_opts['created_since'],
                    fmt="%Y-%m-%d")
            except ValueError:
                msg = date_parsing_error_msg % search_opts['created_since']
                raise exc.HTTPBadRequest(explanation=msg)
            networks = [network for network in networks
                        if network['created_at'] >= created_since]
        if 'created_before' in search_opts:
            try:
                created_before = timeutils.parse_strtime(
                    search_opts['created_before'],
                    fmt="%Y-%m-%d")
            except ValueError:
                msg = date_parsing_error_msg % search_opts['created_before']
                raise exc.HTTPBadRequest(explanation=msg)
            networks = [network for network in networks
                        if network['created_at'] <= created_before]
        opts_to_remove = [
            'all_tenants',
            'created_since',
            'created_before',
            'limit',
            'offset',
            'security_service_id',
            'project_id'
        ]
        for opt in opts_to_remove:
            search_opts.pop(opt, None)
        if search_opts:
            for key, value in search_opts.items():
                if key in ['ip_version', 'segmentation_id']:
                    value = int(value)
                if (req.api_version_request >=
                        api_version.APIVersionRequest("2.36")):
                    networks = [
                        network for network in networks
                        if network.get(key) == value or
                        self._subnet_has_search_opt(key, value, network) or
                        (value in network.get(key.rstrip('~'))
                            if key.endswith('~') and
                            network.get(key.rstrip('~')) else ())]
                else:
                    networks = [
                        network for network in networks
                        if network.get(key) == value or
                        self._subnet_has_search_opt(key, value, network,
                                                    exact_value=True)]

        limited_list = common.limited(networks, req)
        return self._view_builder.build_share_networks(
            req, limited_list, is_detail)

    def _share_network_subnets_contain_share_servers(self, share_network):
        for subnet in share_network['share_network_subnets']:
            if subnet['share_servers'] and len(subnet['share_servers']) > 0:
                return True
        return False

    def index(self, req):
        """Returns a summary list of share networks."""
        policy.check_policy(req.environ['manila.context'], RESOURCE_NAME,
                            'index')
        return self._get_share_networks(req, is_detail=False)

    def detail(self, req):
        """Returns a detailed list of share networks."""
        policy.check_policy(req.environ['manila.context'], RESOURCE_NAME,
                            'detail')
        return self._get_share_networks(req)

    def update(self, req, id, body):
        """Update specified share network."""
        context = req.environ['manila.context']
        policy.check_policy(context, RESOURCE_NAME, 'update')

        if not body or RESOURCE_NAME not in body:
            raise exc.HTTPUnprocessableEntity()

        try:
            share_network = db_api.share_network_get(context, id)
        except exception.ShareNetworkNotFound as e:
            raise exc.HTTPNotFound(explanation=six.text_type(e))

        update_values = body[RESOURCE_NAME]

        if 'nova_net_id' in update_values:
            msg = _("nova networking is not supported starting in Ocata.")
            raise exc.HTTPBadRequest(explanation=msg)

        if self._share_network_subnets_contain_share_servers(share_network):
            for value in update_values:
                if value not in ['name', 'description']:
                    msg = (_("Cannot update share network %s. It is used by "
                             "share servers. Only 'name' and 'description' "
                             "fields are available for update") %
                           share_network['id'])
                    raise exc.HTTPForbidden(explanation=msg)
        try:
            if ('neutron_net_id' in update_values or
                    'neutron_subnet_id' in update_values):
                subnet = db_api.share_network_subnet_get_default_subnet(
                    context, id)
                if not subnet:
                    msg = _("The share network %(id)s does not have a "
                            "'default' subnet that serves all availability "
                            "zones, so subnet details "
                            "('neutron_net_id', 'neutron_subnet_id') cannot "
                            "be updated.") % {'id': id}
                    raise exc.HTTPBadRequest(explanation=msg)

                # NOTE(silvacarlose): If the default share network subnet have
                # the fields neutron_net_id and neutron_subnet_id set as None,
                # we need to make sure that in the update request the user is
                # passing both parameter since a share network subnet must
                # have both fields filled or empty.
                subnet_neutron_net_and_subnet_id_are_empty = (
                    subnet['neutron_net_id'] is None
                    and subnet['neutron_subnet_id'] is None)
                update_values_without_neutron_net_or_subnet = (
                    update_values.get('neutron_net_id') is None or
                    update_values.get('neutron_subnet_id') is None)
                if (subnet_neutron_net_and_subnet_id_are_empty
                        and update_values_without_neutron_net_or_subnet):
                    msg = _(
                        "To update the share network %(id)s you need to "
                        "specify both 'neutron_net_id' and "
                        "'neutron_subnet_id'.") % {'id': id}
                    raise webob.exc.HTTPBadRequest(explanation=msg)
                db_api.share_network_subnet_update(context,
                                                   subnet['id'],
                                                   update_values)
            share_network = db_api.share_network_update(context,
                                                        id,
                                                        update_values)
        except db_exception.DBError:
            msg = "Could not save supplied data due to database error"
            raise exc.HTTPBadRequest(explanation=msg)

        return self._view_builder.build_share_network(req, share_network)

    def create(self, req, body):
        """Creates a new share network."""
        context = req.environ['manila.context']
        policy.check_policy(context, RESOURCE_NAME, 'create')

        if not body or RESOURCE_NAME not in body:
            raise exc.HTTPUnprocessableEntity()

        share_network_values = body[RESOURCE_NAME]
        share_network_subnet_values = copy.deepcopy(share_network_values)
        share_network_values['project_id'] = context.project_id
        share_network_values['user_id'] = context.user_id

        if 'nova_net_id' in share_network_values:
            msg = _("nova networking is not supported starting in Ocata.")
            raise exc.HTTPBadRequest(explanation=msg)

        share_network_values.pop('availability_zone', None)
        share_network_values.pop('neutron_net_id', None)
        share_network_values.pop('neutron_subnet_id', None)

        if req.api_version_request >= api_version.APIVersionRequest("2.51"):
            if 'availability_zone' in share_network_subnet_values:
                try:
                    az = db_api.availability_zone_get(
                        context,
                        share_network_subnet_values['availability_zone'])
                    share_network_subnet_values['availability_zone_id'] = (
                        az['id'])
                    share_network_subnet_values.pop('availability_zone')
                except exception.AvailabilityZoneNotFound:
                    msg = (_("The provided availability zone %s does not "
                             "exist.")
                           % share_network_subnet_values['availability_zone'])
                    raise exc.HTTPBadRequest(explanation=msg)

        common.check_net_id_and_subnet_id(share_network_subnet_values)

        try:
            reservations = QUOTAS.reserve(context, share_networks=1)
        except exception.OverQuota as e:
            overs = e.kwargs['overs']
            usages = e.kwargs['usages']
            quotas = e.kwargs['quotas']

            def _consumed(name):
                return (usages[name]['reserved'] + usages[name]['in_use'])

            if 'share_networks' in overs:
                LOG.warning("Quota exceeded for %(s_pid)s, "
                            "tried to create "
                            "share-network (%(d_consumed)d of %(d_quota)d "
                            "already consumed).", {
                                's_pid': context.project_id,
                                'd_consumed': _consumed('share_networks'),
                                'd_quota': quotas['share_networks']})
                raise exception.ShareNetworksLimitExceeded(
                    allowed=quotas['share_networks'])
        else:
            # Tries to create the new share network
            try:
                share_network = db_api.share_network_create(
                    context, share_network_values)
            except db_exception.DBError as e:
                LOG.exception(e)
                msg = "Could not create share network."
                raise exc.HTTPInternalServerError(explanation=msg)

            share_network_subnet_values['share_network_id'] = (
                share_network['id'])
            share_network_subnet_values.pop('id', None)

            # Try to create the share network subnet. If it fails, the service
            # must rollback the share network creation.
            try:
                db_api.share_network_subnet_create(
                    context, share_network_subnet_values)
            except db_exception.DBError:
                db_api.share_network_delete(context, share_network['id'])
                msg = _('Could not create share network.')
                raise exc.HTTPInternalServerError(explanation=msg)

            QUOTAS.commit(context, reservations)
            share_network = db_api.share_network_get(context,
                                                     share_network['id'])
            return self._view_builder.build_share_network(req, share_network)

    def action(self, req, id, body):
        _actions = {
            'add_security_service': self._add_security_service,
            'remove_security_service': self._remove_security_service
        }
        for action, data in body.items():
            try:
                return _actions[action](req, id, data)
            except KeyError:
                msg = _("Share networks does not have %s action") % action
                raise exc.HTTPBadRequest(explanation=msg)

    def _add_security_service(self, req, id, data):
        """Associate share network with a given security service."""
        context = req.environ['manila.context']
        policy.check_policy(context, RESOURCE_NAME, 'add_security_service')
        share_network = db_api.share_network_get(context, id)
        if self._share_network_subnets_contain_share_servers(share_network):
            msg = _("Cannot add security services. Share network is used.")
            raise exc.HTTPForbidden(explanation=msg)
        security_service = db_api.security_service_get(
            context, data['security_service_id'])
        for attached_service in share_network['security_services']:
            if attached_service['type'] == security_service['type']:
                msg = _("Cannot add security service to share network. "
                        "Security service with '%(ss_type)s' type already "
                        "added to '%(sn_id)s' share network") % {
                            'ss_type': security_service['type'],
                            'sn_id': share_network['id']}
                raise exc.HTTPConflict(explanation=msg)
        try:
            share_network = db_api.share_network_add_security_service(
                context,
                id,
                data['security_service_id'])
        except KeyError:
            msg = "Malformed request body"
            raise exc.HTTPBadRequest(explanation=msg)
        except exception.NotFound as e:
            raise exc.HTTPNotFound(explanation=six.text_type(e))
        except exception.ShareNetworkSecurityServiceAssociationError as e:
            raise exc.HTTPBadRequest(explanation=six.text_type(e))

        return self._view_builder.build_share_network(req, share_network)

    def _remove_security_service(self, req, id, data):
        """Dissociate share network from a given security service."""
        context = req.environ['manila.context']
        policy.check_policy(context, RESOURCE_NAME, 'remove_security_service')
        share_network = db_api.share_network_get(context, id)

        if self._share_network_subnets_contain_share_servers(share_network):
            msg = _("Cannot remove security services. Share network is used.")
            raise exc.HTTPForbidden(explanation=msg)
        try:
            share_network = db_api.share_network_remove_security_service(
                context,
                id,
                data['security_service_id'])
        except KeyError:
            msg = "Malformed request body"
            raise exc.HTTPBadRequest(explanation=msg)
        except exception.NotFound as e:
            raise exc.HTTPNotFound(explanation=six.text_type(e))
        except exception.ShareNetworkSecurityServiceDissociationError as e:
            raise exc.HTTPBadRequest(explanation=six.text_type(e))

        return self._view_builder.build_share_network(req, share_network)


def create_resource():
    return wsgi.Resource(ShareNetworkController())
