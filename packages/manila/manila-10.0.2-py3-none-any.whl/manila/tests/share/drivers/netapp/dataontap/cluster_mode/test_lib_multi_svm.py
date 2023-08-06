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
Unit tests for the NetApp Data ONTAP cDOT multi-SVM storage driver library.
"""

import copy
from unittest import mock

import ddt
from oslo_log import log
from oslo_serialization import jsonutils

from manila.common import constants
from manila import context
from manila import exception
from manila.share.drivers.netapp.dataontap.client import api as netapp_api
from manila.share.drivers.netapp.dataontap.cluster_mode import data_motion
from manila.share.drivers.netapp.dataontap.cluster_mode import lib_base
from manila.share.drivers.netapp.dataontap.cluster_mode import lib_multi_svm
from manila.share.drivers.netapp import utils as na_utils
from manila.share import utils as share_utils
from manila import test
from manila.tests.share.drivers.netapp.dataontap.client import fakes as c_fake
from manila.tests.share.drivers.netapp.dataontap import fakes as fake


@ddt.ddt
class NetAppFileStorageLibraryTestCase(test.TestCase):

    def setUp(self):
        super(NetAppFileStorageLibraryTestCase, self).setUp()

        self.mock_object(na_utils, 'validate_driver_instantiation')

        # Mock loggers as themselves to allow logger arg validation
        mock_logger = log.getLogger('mock_logger')
        self.mock_object(lib_multi_svm.LOG,
                         'warning',
                         mock.Mock(side_effect=mock_logger.warning))
        self.mock_object(lib_multi_svm.LOG,
                         'error',
                         mock.Mock(side_effect=mock_logger.error))

        kwargs = {
            'configuration': fake.get_config_cmode(),
            'private_storage': mock.Mock(),
            'app_version': fake.APP_VERSION
        }

        self.library = lib_multi_svm.NetAppCmodeMultiSVMFileStorageLibrary(
            fake.DRIVER_NAME, **kwargs)
        self.library._client = mock.Mock()
        self.library._client.get_ontapi_version.return_value = (1, 21)
        self.client = self.library._client
        self.fake_new_replica = copy.deepcopy(fake.SHARE)
        self.fake_new_ss = copy.deepcopy(fake.SHARE_SERVER)
        self.fake_new_vserver_name = 'fake_new_vserver'
        self.fake_new_ss['backend_details']['vserver_name'] = (
            self.fake_new_vserver_name
        )
        self.fake_new_replica['share_server'] = self.fake_new_ss
        self.fake_new_replica_host = 'fake_new_host'
        self.fake_replica = copy.deepcopy(fake.SHARE)
        self.fake_replica['id'] = fake.SHARE_ID2
        fake_ss = copy.deepcopy(fake.SHARE_SERVER)
        self.fake_vserver = 'fake_vserver'
        fake_ss['backend_details']['vserver_name'] = (
            self.fake_vserver
        )
        self.fake_replica['share_server'] = fake_ss
        self.fake_replica_host = 'fake_host'

        self.fake_new_client = mock.Mock()
        self.fake_client = mock.Mock()

    def test_check_for_setup_error_cluster_creds_no_vserver(self):
        self.library._have_cluster_creds = True
        self.mock_object(self.library,
                         '_find_matching_aggregates',
                         mock.Mock(return_value=fake.AGGREGATES))
        mock_super = self.mock_object(lib_base.NetAppCmodeFileStorageLibrary,
                                      'check_for_setup_error')

        self.library.check_for_setup_error()

        self.assertTrue(self.library._find_matching_aggregates.called)
        mock_super.assert_called_once_with()

    def test_check_for_setup_error_cluster_creds_with_vserver(self):
        self.library._have_cluster_creds = True
        self.library.configuration.netapp_vserver = fake.VSERVER1
        self.mock_object(self.library,
                         '_find_matching_aggregates',
                         mock.Mock(return_value=fake.AGGREGATES))
        mock_super = self.mock_object(lib_base.NetAppCmodeFileStorageLibrary,
                                      'check_for_setup_error')

        self.library.check_for_setup_error()

        mock_super.assert_called_once_with()
        self.assertTrue(self.library._find_matching_aggregates.called)
        self.assertTrue(lib_multi_svm.LOG.warning.called)

    def test_check_for_setup_error_vserver_creds(self):
        self.library._have_cluster_creds = False

        self.assertRaises(exception.InvalidInput,
                          self.library.check_for_setup_error)

    def test_check_for_setup_error_no_aggregates(self):
        self.library._have_cluster_creds = True
        self.mock_object(self.library,
                         '_find_matching_aggregates',
                         mock.Mock(return_value=[]))

        self.assertRaises(exception.NetAppException,
                          self.library.check_for_setup_error)
        self.assertTrue(self.library._find_matching_aggregates.called)

    def test_get_vserver_no_share_server(self):

        self.assertRaises(exception.InvalidInput,
                          self.library._get_vserver)

    def test_get_vserver_no_share_server_with_vserver_name(self):
        fake_vserver_client = 'fake_client'

        mock_vserver_exists = self.mock_object(
            self.library._client, 'vserver_exists',
            mock.Mock(return_value=True))
        self.mock_object(self.library,
                         '_get_api_client',
                         mock.Mock(return_value=fake_vserver_client))

        result_vserver, result_vserver_client = self.library._get_vserver(
            share_server=None, vserver_name=fake.VSERVER1)

        mock_vserver_exists.assert_called_once_with(
            fake.VSERVER1
        )
        self.assertEqual(fake.VSERVER1, result_vserver)
        self.assertEqual(fake_vserver_client, result_vserver_client)

    def test_get_vserver_no_backend_details(self):

        fake_share_server = copy.deepcopy(fake.SHARE_SERVER)
        fake_share_server.pop('backend_details')
        kwargs = {'share_server': fake_share_server}

        self.assertRaises(exception.VserverNotSpecified,
                          self.library._get_vserver,
                          **kwargs)

    def test_get_vserver_none_backend_details(self):

        fake_share_server = copy.deepcopy(fake.SHARE_SERVER)
        fake_share_server['backend_details'] = None
        kwargs = {'share_server': fake_share_server}

        self.assertRaises(exception.VserverNotSpecified,
                          self.library._get_vserver,
                          **kwargs)

    def test_get_vserver_no_vserver(self):

        fake_share_server = copy.deepcopy(fake.SHARE_SERVER)
        fake_share_server['backend_details'].pop('vserver_name')
        kwargs = {'share_server': fake_share_server}

        self.assertRaises(exception.VserverNotSpecified,
                          self.library._get_vserver,
                          **kwargs)

    def test_get_vserver_none_vserver(self):

        fake_share_server = copy.deepcopy(fake.SHARE_SERVER)
        fake_share_server['backend_details']['vserver_name'] = None
        kwargs = {'share_server': fake_share_server}

        self.assertRaises(exception.VserverNotSpecified,
                          self.library._get_vserver,
                          **kwargs)

    def test_get_vserver_not_found(self):

        self.library._client.vserver_exists.return_value = False
        kwargs = {'share_server': fake.SHARE_SERVER}

        self.assertRaises(exception.VserverNotFound,
                          self.library._get_vserver,
                          **kwargs)

    def test_get_vserver(self):

        self.library._client.vserver_exists.return_value = True
        self.mock_object(self.library,
                         '_get_api_client',
                         mock.Mock(return_value='fake_client'))

        result = self.library._get_vserver(share_server=fake.SHARE_SERVER)

        self.assertTupleEqual((fake.VSERVER1, 'fake_client'), result)

    def test_get_ems_pool_info(self):

        self.mock_object(self.library,
                         '_find_matching_aggregates',
                         mock.Mock(return_value=['aggr1', 'aggr2']))

        result = self.library._get_ems_pool_info()

        expected = {
            'pools': {
                'vserver': None,
                'aggregates': ['aggr1', 'aggr2'],
            },
        }
        self.assertEqual(expected, result)

    @ddt.data('fake', fake.IDENTIFIER)
    def test_manage_server(self, fake_vserver_name):

        self.mock_object(context,
                         'get_admin_context',
                         mock.Mock(return_value='fake_admin_context'))
        mock_get_vserver_name = self.mock_object(
            self.library, '_get_vserver_name',
            mock.Mock(return_value=fake_vserver_name))

        new_identifier, new_details = self.library.manage_server(
            context, fake.SHARE_SERVER, fake.IDENTIFIER, {})

        mock_get_vserver_name.assert_called_once_with(fake.SHARE_SERVER['id'])
        self.assertEqual(fake_vserver_name, new_details['vserver_name'])
        self.assertEqual(fake_vserver_name, new_identifier)

    def test_get_share_server_network_info(self):

        fake_vserver_client = mock.Mock()

        self.mock_object(context,
                         'get_admin_context',
                         mock.Mock(return_value='fake_admin_context'))
        mock_get_vserver = self.mock_object(
            self.library, '_get_vserver',
            mock.Mock(return_value=['fake', fake_vserver_client]))

        net_interfaces = copy.deepcopy(c_fake.NETWORK_INTERFACES_MULTIPLE)

        self.mock_object(fake_vserver_client,
                         'get_network_interfaces',
                         mock.Mock(return_value=net_interfaces))

        result = self.library.get_share_server_network_info(context,
                                                            fake.SHARE_SERVER,
                                                            fake.IDENTIFIER,
                                                            {})
        mock_get_vserver.assert_called_once_with(
            vserver_name=fake.IDENTIFIER
        )
        reference_allocations = []
        for lif in net_interfaces:
            reference_allocations.append(lif['address'])

        self.assertEqual(reference_allocations, result)

    @ddt.data((True, fake.IDENTIFIER),
              (False, fake.IDENTIFIER))
    @ddt.unpack
    def test__verify_share_server_name(self, vserver_exists, identifier):

        mock_exists = self.mock_object(self.client, 'vserver_exists',
                                       mock.Mock(return_value=vserver_exists))
        expected_result = identifier
        if not vserver_exists:
            expected_result = self.library._get_vserver_name(identifier)

        result = self.library._get_correct_vserver_old_name(identifier)

        self.assertEqual(result, expected_result)
        mock_exists.assert_called_once_with(identifier)

    def test_handle_housekeeping_tasks(self):

        self.mock_object(self.client, 'prune_deleted_nfs_export_policies')
        self.mock_object(self.client, 'prune_deleted_snapshots')
        mock_super = self.mock_object(lib_base.NetAppCmodeFileStorageLibrary,
                                      '_handle_housekeeping_tasks')

        self.library._handle_housekeeping_tasks()

        self.assertTrue(self.client.prune_deleted_nfs_export_policies.called)
        self.assertTrue(self.client.prune_deleted_snapshots.called)
        self.assertTrue(mock_super.called)

    def test_find_matching_aggregates(self):

        mock_list_non_root_aggregates = self.mock_object(
            self.client, 'list_non_root_aggregates',
            mock.Mock(return_value=fake.AGGREGATES))
        self.library.configuration.netapp_aggregate_name_search_pattern = (
            '.*_aggr_1')

        result = self.library._find_matching_aggregates()

        self.assertListEqual([fake.AGGREGATES[0]], result)
        mock_list_non_root_aggregates.assert_called_once_with()

    def test_setup_server(self):

        mock_get_vserver_name = self.mock_object(
            self.library,
            '_get_vserver_name',
            mock.Mock(return_value=fake.VSERVER1))

        mock_create_vserver = self.mock_object(self.library, '_create_vserver')

        mock_validate_network_type = self.mock_object(
            self.library,
            '_validate_network_type')

        result = self.library.setup_server(fake.NETWORK_INFO)

        ports = {}
        for network_allocation in fake.NETWORK_INFO['network_allocations']:
            ports[network_allocation['id']] = network_allocation['ip_address']

        self.assertTrue(mock_validate_network_type.called)
        self.assertTrue(mock_get_vserver_name.called)
        self.assertTrue(mock_create_vserver.called)
        self.assertDictEqual({'vserver_name': fake.VSERVER1,
                              'ports': jsonutils.dumps(ports)}, result)

    def test_setup_server_with_error(self):

        mock_get_vserver_name = self.mock_object(
            self.library,
            '_get_vserver_name',
            mock.Mock(return_value=fake.VSERVER1))

        fake_exception = exception.ManilaException("fake")
        mock_create_vserver = self.mock_object(
            self.library,
            '_create_vserver',
            mock.Mock(side_effect=fake_exception))

        mock_validate_network_type = self.mock_object(
            self.library,
            '_validate_network_type')

        self.assertRaises(
            exception.ManilaException,
            self.library.setup_server,
            fake.NETWORK_INFO)

        ports = {}
        for network_allocation in fake.NETWORK_INFO['network_allocations']:
            ports[network_allocation['id']] = network_allocation['ip_address']

        self.assertTrue(mock_validate_network_type.called)
        self.assertTrue(mock_get_vserver_name.called)
        self.assertTrue(mock_create_vserver.called)
        self.assertDictEqual(
            {'server_details': {'vserver_name': fake.VSERVER1,
                                'ports': jsonutils.dumps(ports)}},
            fake_exception.detail_data)

    @ddt.data(
        {'network_info': {'network_type': 'vlan', 'segmentation_id': 1000}},
        {'network_info': {'network_type': None, 'segmentation_id': None}},
        {'network_info': {'network_type': 'flat', 'segmentation_id': None}})
    @ddt.unpack
    def test_validate_network_type_with_valid_network_types(self,
                                                            network_info):
        self.library._validate_network_type(network_info)

    @ddt.data(
        {'network_info': {'network_type': 'vxlan', 'segmentation_id': 1000}},
        {'network_info': {'network_type': 'gre', 'segmentation_id': 100}})
    @ddt.unpack
    def test_validate_network_type_with_invalid_network_types(self,
                                                              network_info):
        self.assertRaises(exception.NetworkBadConfigurationException,
                          self.library._validate_network_type,
                          network_info)

    def test_get_vserver_name(self):
        vserver_id = fake.NETWORK_INFO['server_id']
        vserver_name = fake.VSERVER_NAME_TEMPLATE % vserver_id

        actual_result = self.library._get_vserver_name(vserver_id)

        self.assertEqual(vserver_name, actual_result)

    @ddt.data(None, fake.IPSPACE)
    def test_create_vserver(self, existing_ipspace):

        versions = ['fake_v1', 'fake_v2']
        self.library.configuration.netapp_enabled_share_protocols = versions
        vserver_id = fake.NETWORK_INFO['server_id']
        vserver_name = fake.VSERVER_NAME_TEMPLATE % vserver_id
        vserver_client = mock.Mock()

        self.mock_object(self.library._client,
                         'list_cluster_nodes',
                         mock.Mock(return_value=fake.CLUSTER_NODES))
        self.mock_object(self.library,
                         '_get_node_data_port',
                         mock.Mock(return_value='fake_port'))
        self.mock_object(context,
                         'get_admin_context',
                         mock.Mock(return_value='fake_admin_context'))
        self.mock_object(self.library,
                         '_get_api_client',
                         mock.Mock(return_value=vserver_client))
        self.mock_object(self.library._client,
                         'vserver_exists',
                         mock.Mock(return_value=False))
        self.mock_object(self.library,
                         '_find_matching_aggregates',
                         mock.Mock(return_value=fake.AGGREGATES))
        self.mock_object(self.library,
                         '_create_ipspace',
                         mock.Mock(return_value=fake.IPSPACE))
        get_ipspace_name_for_vlan_port = self.mock_object(
            self.library._client,
            'get_ipspace_name_for_vlan_port',
            mock.Mock(return_value=existing_ipspace))
        self.mock_object(self.library, '_create_vserver_lifs')
        self.mock_object(self.library, '_create_vserver_admin_lif')
        self.mock_object(self.library, '_create_vserver_routes')

        self.library._create_vserver(vserver_name, fake.NETWORK_INFO)

        get_ipspace_name_for_vlan_port.assert_called_once_with(
            fake.CLUSTER_NODES[0],
            'fake_port',
            fake.NETWORK_INFO['segmentation_id'])
        if not existing_ipspace:
            self.library._create_ipspace.assert_called_once_with(
                fake.NETWORK_INFO)
        self.library._client.create_vserver.assert_called_once_with(
            vserver_name, fake.ROOT_VOLUME_AGGREGATE, fake.ROOT_VOLUME,
            fake.AGGREGATES, fake.IPSPACE)
        self.library._get_api_client.assert_called_once_with(
            vserver=vserver_name)
        self.library._create_vserver_lifs.assert_called_once_with(
            vserver_name, vserver_client, fake.NETWORK_INFO, fake.IPSPACE)
        self.library._create_vserver_admin_lif.assert_called_once_with(
            vserver_name, vserver_client, fake.NETWORK_INFO, fake.IPSPACE)
        self.library._create_vserver_routes.assert_called_once_with(
            vserver_client, fake.NETWORK_INFO)
        vserver_client.enable_nfs.assert_called_once_with(versions)
        self.library._client.setup_security_services.assert_called_once_with(
            fake.NETWORK_INFO['security_services'], vserver_client,
            vserver_name)

    def test_create_vserver_already_present(self):

        vserver_id = fake.NETWORK_INFO['server_id']
        vserver_name = fake.VSERVER_NAME_TEMPLATE % vserver_id

        self.mock_object(context,
                         'get_admin_context',
                         mock.Mock(return_value='fake_admin_context'))
        self.mock_object(self.library._client,
                         'vserver_exists',
                         mock.Mock(return_value=True))

        self.assertRaises(exception.NetAppException,
                          self.library._create_vserver,
                          vserver_name,
                          fake.NETWORK_INFO)

    @ddt.data(
        {'lif_exception': netapp_api.NaApiError,
         'existing_ipspace': fake.IPSPACE},
        {'lif_exception': netapp_api.NaApiError,
         'existing_ipspace': None},
        {'lif_exception': exception.NetAppException,
         'existing_ipspace': None},
        {'lif_exception': exception.NetAppException,
         'existing_ipspace': fake.IPSPACE})
    @ddt.unpack
    def test_create_vserver_lif_creation_failure(self,
                                                 lif_exception,
                                                 existing_ipspace):

        vserver_id = fake.NETWORK_INFO['server_id']
        vserver_name = fake.VSERVER_NAME_TEMPLATE % vserver_id
        vserver_client = mock.Mock()

        self.mock_object(self.library._client,
                         'list_cluster_nodes',
                         mock.Mock(return_value=fake.CLUSTER_NODES))
        self.mock_object(self.library,
                         '_get_node_data_port',
                         mock.Mock(return_value='fake_port'))
        self.mock_object(context,
                         'get_admin_context',
                         mock.Mock(return_value='fake_admin_context'))
        self.mock_object(self.library,
                         '_get_api_client',
                         mock.Mock(return_value=vserver_client))
        self.mock_object(self.library._client,
                         'vserver_exists',
                         mock.Mock(return_value=False))
        self.mock_object(self.library,
                         '_find_matching_aggregates',
                         mock.Mock(return_value=fake.AGGREGATES))
        self.mock_object(self.library._client,
                         'get_ipspace_name_for_vlan_port',
                         mock.Mock(return_value=existing_ipspace))
        self.mock_object(self.library,
                         '_create_ipspace',
                         mock.Mock(return_value=fake.IPSPACE))
        self.mock_object(self.library,
                         '_create_vserver_lifs',
                         mock.Mock(side_effect=lif_exception))
        self.mock_object(self.library, '_delete_vserver')

        self.assertRaises(lif_exception,
                          self.library._create_vserver,
                          vserver_name,
                          fake.NETWORK_INFO)

        self.library._get_api_client.assert_called_with(vserver=vserver_name)
        self.assertTrue(self.library._client.create_vserver.called)
        self.library._create_vserver_lifs.assert_called_with(
            vserver_name,
            vserver_client,
            fake.NETWORK_INFO,
            fake.IPSPACE)
        self.library._delete_vserver.assert_called_once_with(
            vserver_name,
            needs_lock=False,
            security_services=None)
        self.assertFalse(vserver_client.enable_nfs.called)
        self.assertEqual(1, lib_multi_svm.LOG.error.call_count)

    def test_get_valid_ipspace_name(self):

        result = self.library._get_valid_ipspace_name(fake.IPSPACE_ID)

        expected = 'ipspace_' + fake.IPSPACE_ID.replace('-', '_')
        self.assertEqual(expected, result)

    def test_create_ipspace_not_supported(self):

        self.library._client.features.IPSPACES = False

        result = self.library._create_ipspace(fake.NETWORK_INFO)

        self.assertIsNone(result)

    @ddt.data(None, 'flat')
    def test_create_ipspace_not_vlan(self, network_type):

        self.library._client.features.IPSPACES = True
        network_info = copy.deepcopy(fake.NETWORK_INFO)
        network_info['network_allocations'][0]['segmentation_id'] = None
        network_info['network_allocations'][0]['network_type'] = network_type

        result = self.library._create_ipspace(network_info)

        self.assertEqual('Default', result)

    def test_create_ipspace(self):

        self.library._client.features.IPSPACES = True
        self.mock_object(self.library._client,
                         'create_ipspace',
                         mock.Mock(return_value=False))

        result = self.library._create_ipspace(fake.NETWORK_INFO)

        expected = self.library._get_valid_ipspace_name(
            fake.NETWORK_INFO['neutron_subnet_id'])
        self.assertEqual(expected, result)
        self.library._client.create_ipspace.assert_called_once_with(expected)

    def test_create_vserver_lifs(self):

        self.mock_object(self.library._client,
                         'list_cluster_nodes',
                         mock.Mock(return_value=fake.CLUSTER_NODES))
        self.mock_object(self.library,
                         '_get_lif_name',
                         mock.Mock(side_effect=['fake_lif1', 'fake_lif2']))
        self.mock_object(self.library, '_create_lif')

        self.library._create_vserver_lifs(fake.VSERVER1,
                                          'fake_vserver_client',
                                          fake.NETWORK_INFO,
                                          fake.IPSPACE)

        self.library._create_lif.assert_has_calls([
            mock.call('fake_vserver_client', fake.VSERVER1, fake.IPSPACE,
                      fake.CLUSTER_NODES[0], 'fake_lif1',
                      fake.NETWORK_INFO['network_allocations'][0]),
            mock.call('fake_vserver_client', fake.VSERVER1, fake.IPSPACE,
                      fake.CLUSTER_NODES[1], 'fake_lif2',
                      fake.NETWORK_INFO['network_allocations'][1])])

    def test_create_vserver_admin_lif(self):

        self.mock_object(self.library._client,
                         'list_cluster_nodes',
                         mock.Mock(return_value=fake.CLUSTER_NODES))
        self.mock_object(self.library,
                         '_get_lif_name',
                         mock.Mock(return_value='fake_admin_lif'))
        self.mock_object(self.library, '_create_lif')

        self.library._create_vserver_admin_lif(fake.VSERVER1,
                                               'fake_vserver_client',
                                               fake.NETWORK_INFO,
                                               fake.IPSPACE)

        self.library._create_lif.assert_has_calls([
            mock.call('fake_vserver_client', fake.VSERVER1, fake.IPSPACE,
                      fake.CLUSTER_NODES[0], 'fake_admin_lif',
                      fake.NETWORK_INFO['admin_network_allocations'][0])])

    def test_create_vserver_admin_lif_no_admin_network(self):

        fake_network_info = copy.deepcopy(fake.NETWORK_INFO)
        fake_network_info['admin_network_allocations'] = []

        self.mock_object(self.library._client,
                         'list_cluster_nodes',
                         mock.Mock(return_value=fake.CLUSTER_NODES))
        self.mock_object(self.library,
                         '_get_lif_name',
                         mock.Mock(return_value='fake_admin_lif'))
        self.mock_object(self.library, '_create_lif')

        self.library._create_vserver_admin_lif(fake.VSERVER1,
                                               'fake_vserver_client',
                                               fake_network_info,
                                               fake.IPSPACE)

        self.assertFalse(self.library._create_lif.called)

    @ddt.data(
        fake.get_network_info(fake.USER_NETWORK_ALLOCATIONS,
                              fake.ADMIN_NETWORK_ALLOCATIONS),
        fake.get_network_info(fake.USER_NETWORK_ALLOCATIONS_IPV6,
                              fake.ADMIN_NETWORK_ALLOCATIONS))
    def test_create_vserver_routes(self, network_info):
        expected_gateway = network_info['network_allocations'][0]['gateway']
        vserver_client = mock.Mock()
        self.mock_object(vserver_client, 'create_route')

        retval = self.library._create_vserver_routes(
            vserver_client, network_info)

        self.assertIsNone(retval)
        vserver_client.create_route.assert_called_once_with(expected_gateway)

    def test_get_node_data_port(self):

        self.mock_object(self.client,
                         'list_node_data_ports',
                         mock.Mock(return_value=fake.NODE_DATA_PORTS))
        self.library.configuration.netapp_port_name_search_pattern = 'e0c'

        result = self.library._get_node_data_port(fake.CLUSTER_NODE)

        self.assertEqual('e0c', result)
        self.library._client.list_node_data_ports.assert_has_calls([
            mock.call(fake.CLUSTER_NODE)])

    def test_get_node_data_port_no_match(self):

        self.mock_object(self.client,
                         'list_node_data_ports',
                         mock.Mock(return_value=fake.NODE_DATA_PORTS))
        self.library.configuration.netapp_port_name_search_pattern = 'ifgroup1'

        self.assertRaises(exception.NetAppException,
                          self.library._get_node_data_port,
                          fake.CLUSTER_NODE)

    def test_get_lif_name(self):

        result = self.library._get_lif_name(
            'fake_node', fake.NETWORK_INFO['network_allocations'][0])

        self.assertEqual('os_132dbb10-9a36-46f2-8d89-3d909830c356', result)

    @ddt.data(fake.MTU, None, 'not-present')
    def test_create_lif(self, mtu):
        """Tests cases where MTU is a valid value, None or not present."""

        expected_mtu = (mtu if mtu not in (None, 'not-present') else
                        fake.DEFAULT_MTU)

        network_allocations = copy.deepcopy(
            fake.NETWORK_INFO['network_allocations'][0])
        network_allocations['mtu'] = mtu

        if mtu == 'not-present':
            network_allocations.pop('mtu')

        vserver_client = mock.Mock()
        vserver_client.network_interface_exists = mock.Mock(
            return_value=False)
        self.mock_object(self.library,
                         '_get_node_data_port',
                         mock.Mock(return_value='fake_port'))

        self.library._create_lif(vserver_client,
                                 'fake_vserver',
                                 'fake_ipspace',
                                 'fake_node',
                                 'fake_lif',
                                 network_allocations)

        self.library._client.create_network_interface.assert_has_calls([
            mock.call('10.10.10.10', '255.255.255.0', '1000', 'fake_node',
                      'fake_port', 'fake_vserver', 'fake_lif',
                      'fake_ipspace', expected_mtu)])

    def test_create_lif_if_nonexistent_already_present(self):

        vserver_client = mock.Mock()
        vserver_client.network_interface_exists = mock.Mock(
            return_value=True)
        self.mock_object(self.library,
                         '_get_node_data_port',
                         mock.Mock(return_value='fake_port'))

        self.library._create_lif(vserver_client,
                                 'fake_vserver',
                                 fake.IPSPACE,
                                 'fake_node',
                                 'fake_lif',
                                 fake.NETWORK_INFO['network_allocations'][0])

        self.assertFalse(self.library._client.create_network_interface.called)

    def test_get_network_allocations_number(self):

        self.library._client.list_cluster_nodes.return_value = (
            fake.CLUSTER_NODES)

        result = self.library.get_network_allocations_number()

        self.assertEqual(len(fake.CLUSTER_NODES), result)

    def test_get_admin_network_allocations_number(self):

        result = self.library.get_admin_network_allocations_number(
            'fake_admin_network_api')

        self.assertEqual(1, result)

    def test_get_admin_network_allocations_number_no_admin_network(self):

        result = self.library.get_admin_network_allocations_number(None)

        self.assertEqual(0, result)

    def test_teardown_server(self):

        self.library._client.vserver_exists.return_value = True
        mock_delete_vserver = self.mock_object(self.library,
                                               '_delete_vserver')

        self.library.teardown_server(
            fake.SHARE_SERVER['backend_details'],
            security_services=fake.NETWORK_INFO['security_services'])

        self.library._client.vserver_exists.assert_called_once_with(
            fake.VSERVER1)
        mock_delete_vserver.assert_called_once_with(
            fake.VSERVER1,
            security_services=fake.NETWORK_INFO['security_services'])

    @ddt.data(None, {}, {'vserver_name': None})
    def test_teardown_server_no_share_server(self, server_details):

        mock_delete_vserver = self.mock_object(self.library,
                                               '_delete_vserver')

        self.library.teardown_server(server_details)

        self.assertFalse(mock_delete_vserver.called)
        self.assertTrue(lib_multi_svm.LOG.warning.called)

    def test_teardown_server_no_vserver(self):

        self.library._client.vserver_exists.return_value = False
        mock_delete_vserver = self.mock_object(self.library,
                                               '_delete_vserver')

        self.library.teardown_server(
            fake.SHARE_SERVER['backend_details'],
            security_services=fake.NETWORK_INFO['security_services'])

        self.library._client.vserver_exists.assert_called_once_with(
            fake.VSERVER1)
        self.assertFalse(mock_delete_vserver.called)
        self.assertTrue(lib_multi_svm.LOG.warning.called)

    @ddt.data(True, False)
    def test_delete_vserver_no_ipspace(self, lock):

        self.mock_object(self.library._client,
                         'get_vserver_ipspace',
                         mock.Mock(return_value=None))
        vserver_client = mock.Mock()
        self.mock_object(self.library,
                         '_get_api_client',
                         mock.Mock(return_value=vserver_client))
        mock_delete_vserver_vlans = self.mock_object(self.library,
                                                     '_delete_vserver_vlans')

        net_interfaces = copy.deepcopy(c_fake.NETWORK_INTERFACES_MULTIPLE)
        net_interfaces_with_vlans = [net_interfaces[0]]

        self.mock_object(vserver_client,
                         'get_network_interfaces',
                         mock.Mock(return_value=net_interfaces))
        security_services = fake.NETWORK_INFO['security_services']
        self.mock_object(self.library, '_delete_vserver_peers')

        self.library._delete_vserver(fake.VSERVER1,
                                     security_services=security_services,
                                     needs_lock=lock)

        self.library._client.get_vserver_ipspace.assert_called_once_with(
            fake.VSERVER1)
        self.library._delete_vserver_peers.assert_called_once_with(
            fake.VSERVER1)
        self.library._client.delete_vserver.assert_called_once_with(
            fake.VSERVER1, vserver_client, security_services=security_services)
        self.assertFalse(self.library._client.delete_ipspace.called)
        mock_delete_vserver_vlans.assert_called_once_with(
            net_interfaces_with_vlans)

    @ddt.data(True, False)
    def test_delete_vserver_ipspace_has_data_vservers(self, lock):

        self.mock_object(self.library._client,
                         'get_vserver_ipspace',
                         mock.Mock(return_value=fake.IPSPACE))
        vserver_client = mock.Mock()
        self.mock_object(self.library,
                         '_get_api_client',
                         mock.Mock(return_value=vserver_client))
        self.mock_object(self.library._client,
                         'ipspace_has_data_vservers',
                         mock.Mock(return_value=True))
        mock_delete_vserver_vlans = self.mock_object(self.library,
                                                     '_delete_vserver_vlans')
        self.mock_object(self.library, '_delete_vserver_peers')
        self.mock_object(
            vserver_client, 'get_network_interfaces',
            mock.Mock(return_value=c_fake.NETWORK_INTERFACES_MULTIPLE))
        security_services = fake.NETWORK_INFO['security_services']

        self.library._delete_vserver(fake.VSERVER1,
                                     security_services=security_services,
                                     needs_lock=lock)

        self.library._client.get_vserver_ipspace.assert_called_once_with(
            fake.VSERVER1)
        self.library._client.delete_vserver.assert_called_once_with(
            fake.VSERVER1, vserver_client, security_services=security_services)
        self.library._delete_vserver_peers.assert_called_once_with(
            fake.VSERVER1)
        self.assertFalse(self.library._client.delete_ipspace.called)
        mock_delete_vserver_vlans.assert_called_once_with(
            [c_fake.NETWORK_INTERFACES_MULTIPLE[0]])

    @ddt.data([], c_fake.NETWORK_INTERFACES)
    def test_delete_vserver_with_ipspace(self, interfaces):

        self.mock_object(self.library._client,
                         'get_vserver_ipspace',
                         mock.Mock(return_value=fake.IPSPACE))
        vserver_client = mock.Mock()
        self.mock_object(self.library,
                         '_get_api_client',
                         mock.Mock(return_value=vserver_client))
        self.mock_object(self.library._client,
                         'ipspace_has_data_vservers',
                         mock.Mock(return_value=False))
        mock_delete_vserver_vlans = self.mock_object(self.library,
                                                     '_delete_vserver_vlans')
        self.mock_object(self.library, '_delete_vserver_peers')
        self.mock_object(vserver_client,
                         'get_network_interfaces',
                         mock.Mock(return_value=interfaces))

        security_services = fake.NETWORK_INFO['security_services']

        self.library._delete_vserver(fake.VSERVER1,
                                     security_services=security_services)
        self.library._delete_vserver_peers.assert_called_once_with(
            fake.VSERVER1
        )
        self.library._client.get_vserver_ipspace.assert_called_once_with(
            fake.VSERVER1)
        self.library._client.delete_vserver.assert_called_once_with(
            fake.VSERVER1, vserver_client, security_services=security_services)
        self.library._client.delete_ipspace.assert_called_once_with(
            fake.IPSPACE)
        mock_delete_vserver_vlans.assert_called_once_with(interfaces)

    def test__delete_vserver_peers(self):

        self.mock_object(self.library,
                         '_get_vserver_peers',
                         mock.Mock(return_value=fake.VSERVER_PEER))
        self.mock_object(self.library, '_delete_vserver_peer')

        self.library._delete_vserver_peers(fake.VSERVER1)

        self.library._get_vserver_peers.assert_called_once_with(
            vserver=fake.VSERVER1
        )
        self.library._delete_vserver_peer.assert_called_once_with(
            fake.VSERVER_PEER[0]['vserver'],
            fake.VSERVER_PEER[0]['peer-vserver']
        )

    def test_delete_vserver_vlans(self):

        self.library._delete_vserver_vlans(c_fake.NETWORK_INTERFACES)
        for interface in c_fake.NETWORK_INTERFACES:
            home_port = interface['home-port']
            port, vlan = home_port.split('-')
            node = interface['home-node']
            self.library._client.delete_vlan.assert_called_once_with(
                node, port, vlan)

    def test_delete_vserver_vlans_client_error(self):

        mock_exception_log = self.mock_object(lib_multi_svm.LOG, 'exception')
        self.mock_object(
            self.library._client,
            'delete_vlan',
            mock.Mock(side_effect=exception.NetAppException("fake error")))

        self.library._delete_vserver_vlans(c_fake.NETWORK_INTERFACES)
        for interface in c_fake.NETWORK_INTERFACES:
            home_port = interface['home-port']
            port, vlan = home_port.split('-')
            node = interface['home-node']
            self.library._client.delete_vlan.assert_called_once_with(
                node, port, vlan)
            self.assertEqual(1, mock_exception_log.call_count)

    @ddt.data([], [{'vserver': c_fake.VSERVER_NAME,
                    'peer-vserver': c_fake.VSERVER_PEER_NAME,
                    'applications': [
                        {'vserver-peer-application': 'snapmirror'}]
                    }])
    def test_create_replica(self, vserver_peers):
        fake_cluster_name = 'fake_cluster'
        self.mock_object(self.library, '_get_vservers_from_replicas',
                         mock.Mock(return_value=(self.fake_vserver,
                                                 self.fake_new_vserver_name)))
        self.mock_object(self.library, 'find_active_replica',
                         mock.Mock(return_value=self.fake_replica))
        self.mock_object(share_utils, 'extract_host',
                         mock.Mock(side_effect=[self.fake_new_replica_host,
                                                self.fake_replica_host]))
        self.mock_object(data_motion, 'get_client_for_backend',
                         mock.Mock(side_effect=[self.fake_new_client,
                                                self.fake_client]))
        self.mock_object(self.library, '_get_vserver_peers',
                         mock.Mock(return_value=vserver_peers))
        self.mock_object(self.fake_new_client, 'get_cluster_name',
                         mock.Mock(return_value=fake_cluster_name))
        self.mock_object(self.fake_client, 'create_vserver_peer')
        self.mock_object(self.fake_new_client, 'accept_vserver_peer')
        lib_base_model_update = {
            'export_locations': [],
            'replica_state': constants.REPLICA_STATE_OUT_OF_SYNC,
            'access_rules_status': constants.STATUS_ACTIVE,
        }
        self.mock_object(lib_base.NetAppCmodeFileStorageLibrary,
                         'create_replica',
                         mock.Mock(return_value=lib_base_model_update))

        model_update = self.library.create_replica(
            None, [self.fake_replica], self.fake_new_replica, [], [],
            share_server=None)

        self.assertDictMatch(lib_base_model_update, model_update)
        self.library._get_vservers_from_replicas.assert_called_once_with(
            None, [self.fake_replica], self.fake_new_replica
        )
        self.library.find_active_replica.assert_called_once_with(
            [self.fake_replica]
        )
        self.assertEqual(2, share_utils.extract_host.call_count)
        self.assertEqual(2, data_motion.get_client_for_backend.call_count)
        self.library._get_vserver_peers.assert_called_once_with(
            self.fake_new_vserver_name, self.fake_vserver
        )
        self.fake_new_client.get_cluster_name.assert_called_once_with()
        if not vserver_peers:
            self.fake_client.create_vserver_peer.assert_called_once_with(
                self.fake_new_vserver_name, self.fake_vserver,
                peer_cluster_name=fake_cluster_name
            )
            self.fake_new_client.accept_vserver_peer.assert_called_once_with(
                self.fake_vserver, self.fake_new_vserver_name
            )
        base_class = lib_base.NetAppCmodeFileStorageLibrary
        base_class.create_replica.assert_called_once_with(
            None, [self.fake_replica], self.fake_new_replica, [], []
        )

    def test_delete_replica(self):
        base_class = lib_base.NetAppCmodeFileStorageLibrary
        vserver_peers = copy.deepcopy(fake.VSERVER_PEER)
        vserver_peers[0]['vserver'] = self.fake_vserver
        vserver_peers[0]['peer-vserver'] = self.fake_new_vserver_name
        self.mock_object(self.library, '_get_vservers_from_replicas',
                         mock.Mock(return_value=(self.fake_vserver,
                                                 self.fake_new_vserver_name)))
        self.mock_object(base_class, 'delete_replica')
        self.mock_object(self.library, '_get_snapmirrors',
                         mock.Mock(return_value=[]))
        self.mock_object(self.library, '_get_vserver_peers',
                         mock.Mock(return_value=vserver_peers))
        self.mock_object(self.library, '_delete_vserver_peer')

        self.library.delete_replica(None, [self.fake_replica],
                                    self.fake_new_replica, [],
                                    share_server=None)

        self.library._get_vservers_from_replicas.assert_called_once_with(
            None, [self.fake_replica], self.fake_new_replica
        )
        base_class.delete_replica.assert_called_once_with(
            None, [self.fake_replica], self.fake_new_replica, []
        )
        self.library._get_snapmirrors.assert_has_calls(
            [mock.call(self.fake_vserver, self.fake_new_vserver_name),
             mock.call(self.fake_new_vserver_name, self.fake_vserver)]
        )
        self.library._get_vserver_peers.assert_called_once_with(
            self.fake_new_vserver_name, self.fake_vserver
        )
        self.library._delete_vserver_peer.assert_called_once_with(
            self.fake_new_vserver_name, self.fake_vserver
        )

    def test_get_vservers_from_replicas(self):
        self.mock_object(self.library, 'find_active_replica',
                         mock.Mock(return_value=self.fake_replica))

        vserver, peer_vserver = self.library._get_vservers_from_replicas(
            None, [self.fake_replica], self.fake_new_replica)

        self.library.find_active_replica.assert_called_once_with(
            [self.fake_replica]
        )
        self.assertEqual(self.fake_vserver, vserver)
        self.assertEqual(self.fake_new_vserver_name, peer_vserver)

    def test_get_vserver_peers(self):
        self.mock_object(self.library._client, 'get_vserver_peers')

        self.library._get_vserver_peers(
            vserver=self.fake_vserver, peer_vserver=self.fake_new_vserver_name)

        self.library._client.get_vserver_peers.assert_called_once_with(
            self.fake_vserver, self.fake_new_vserver_name
        )

    def test_create_vserver_peer(self):
        self.mock_object(self.library._client, 'create_vserver_peer')

        self.library._create_vserver_peer(
            None, vserver=self.fake_vserver,
            peer_vserver=self.fake_new_vserver_name)

        self.library._client.create_vserver_peer.assert_called_once_with(
            self.fake_vserver, self.fake_new_vserver_name
        )

    def test_delete_vserver_peer(self):
        self.mock_object(self.library._client, 'delete_vserver_peer')

        self.library._delete_vserver_peer(
            vserver=self.fake_vserver, peer_vserver=self.fake_new_vserver_name)

        self.library._client.delete_vserver_peer.assert_called_once_with(
            self.fake_vserver, self.fake_new_vserver_name
        )

    def test_create_share_from_snaphot(self):
        fake_parent_share = copy.deepcopy(fake.SHARE)
        fake_parent_share['id'] = fake.SHARE_ID2
        mock_create_from_snap = self.mock_object(
            lib_base.NetAppCmodeFileStorageLibrary,
            'create_share_from_snapshot')

        self.library.create_share_from_snapshot(
            None, fake.SHARE, fake.SNAPSHOT, share_server=fake.SHARE_SERVER,
            parent_share=fake_parent_share)

        mock_create_from_snap.assert_called_once_with(
            None, fake.SHARE, fake.SNAPSHOT, share_server=fake.SHARE_SERVER,
            parent_share=fake_parent_share
        )

    @ddt.data(
        {'src_cluster_name': fake.CLUSTER_NAME,
         'dest_cluster_name': fake.CLUSTER_NAME, 'has_vserver_peers': None},
        {'src_cluster_name': fake.CLUSTER_NAME,
         'dest_cluster_name': fake.CLUSTER_NAME_2, 'has_vserver_peers': False},
        {'src_cluster_name': fake.CLUSTER_NAME,
         'dest_cluster_name': fake.CLUSTER_NAME_2, 'has_vserver_peers': True}
    )
    @ddt.unpack
    def test_create_share_from_snaphot_different_hosts(self, src_cluster_name,
                                                       dest_cluster_name,
                                                       has_vserver_peers):
        class FakeDBObj(dict):
            def to_dict(self):
                return self
        fake_parent_share = copy.deepcopy(fake.SHARE)
        fake_parent_share['id'] = fake.SHARE_ID2
        fake_parent_share['host'] = fake.MANILA_HOST_NAME_2
        fake_share = FakeDBObj(fake.SHARE)
        fake_share_server = FakeDBObj(fake.SHARE_SERVER)
        src_vserver = fake.VSERVER2
        dest_vserver = fake.VSERVER1
        src_backend = fake.BACKEND_NAME
        dest_backend = fake.BACKEND_NAME_2
        mock_dm_session = mock.Mock()

        mock_dm_constr = self.mock_object(
            data_motion, "DataMotionSession",
            mock.Mock(return_value=mock_dm_session))
        mock_get_vserver = self.mock_object(
            mock_dm_session, 'get_vserver_from_share',
            mock.Mock(side_effect=[src_vserver, dest_vserver]))
        src_vserver_client = mock.Mock()
        dest_vserver_client = mock.Mock()
        mock_extract_host = self.mock_object(
            share_utils, 'extract_host',
            mock.Mock(side_effect=[src_backend, dest_backend]))
        mock_dm_get_client = self.mock_object(
            data_motion, 'get_client_for_backend',
            mock.Mock(side_effect=[src_vserver_client, dest_vserver_client]))
        mock_get_src_cluster_name = self.mock_object(
            src_vserver_client, 'get_cluster_name',
            mock.Mock(return_value=src_cluster_name))
        mock_get_dest_cluster_name = self.mock_object(
            dest_vserver_client, 'get_cluster_name',
            mock.Mock(return_value=dest_cluster_name))
        mock_get_vserver_peers = self.mock_object(
            self.library, '_get_vserver_peers',
            mock.Mock(return_value=has_vserver_peers))
        mock_create_vserver_peer = self.mock_object(dest_vserver_client,
                                                    'create_vserver_peer')
        mock_accept_peer = self.mock_object(src_vserver_client,
                                            'accept_vserver_peer')
        mock_create_from_snap = self.mock_object(
            lib_base.NetAppCmodeFileStorageLibrary,
            'create_share_from_snapshot')

        self.library.create_share_from_snapshot(
            None, fake_share, fake.SNAPSHOT, share_server=fake_share_server,
            parent_share=fake_parent_share)

        internal_share = copy.deepcopy(fake.SHARE)
        internal_share['share_server'] = copy.deepcopy(fake.SHARE_SERVER)

        mock_dm_constr.assert_called_once()
        mock_get_vserver.assert_has_calls([mock.call(fake_parent_share),
                                           mock.call(internal_share)])
        mock_extract_host.assert_has_calls([
            mock.call(fake_parent_share['host'], level='backend_name'),
            mock.call(internal_share['host'], level='backend_name')])
        mock_dm_get_client.assert_has_calls([
            mock.call(src_backend, vserver_name=src_vserver),
            mock.call(dest_backend, vserver_name=dest_vserver)
        ])
        mock_get_src_cluster_name.assert_called_once()
        mock_get_dest_cluster_name.assert_called_once()
        if src_cluster_name != dest_cluster_name:
            mock_get_vserver_peers.assert_called_once_with(dest_vserver,
                                                           src_vserver)
            if not has_vserver_peers:
                mock_create_vserver_peer.assert_called_once_with(
                    dest_vserver, src_vserver,
                    peer_cluster_name=src_cluster_name)
                mock_accept_peer.assert_called_once_with(src_vserver,
                                                         dest_vserver)
        mock_create_from_snap.assert_called_once_with(
            None, fake.SHARE, fake.SNAPSHOT, share_server=fake.SHARE_SERVER,
            parent_share=fake_parent_share)
