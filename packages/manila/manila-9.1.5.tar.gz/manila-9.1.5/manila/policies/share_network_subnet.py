# Copyright 2019 NetApp, Inc.
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

from oslo_policy import policy

from manila.policies import base

BASE_POLICY_NAME = 'share_network_subnet:%s'


share_network_subnet_policies = [
    policy.DocumentedRuleDefault(
        name=BASE_POLICY_NAME % 'create',
        check_str=base.RULE_DEFAULT,
        description="Create a new share network subnet.",
        operations=[
            {
                'method': 'POST',
                'path': '/share-networks/{share_network_id}/subnets'
            }
        ]),
    policy.DocumentedRuleDefault(
        name=BASE_POLICY_NAME % 'delete',
        check_str=base.RULE_DEFAULT,
        description="Delete a share network subnet.",
        operations=[
            {
                'method': 'DELETE',
                'path': '/share-networks/{share_network_id}/subnets/'
                        '{share_network_subnet_id}'
            }
        ]),
    policy.DocumentedRuleDefault(
        name=BASE_POLICY_NAME % 'show',
        check_str=base.RULE_DEFAULT,
        description="Shows a share network subnet.",
        operations=[
            {
                'method': 'GET',
                'path': '/share-networks/{share_network_id}/subnets/'
                        '{share_network_subnet_id}'
            }
        ]),
    policy.DocumentedRuleDefault(
        name=BASE_POLICY_NAME % 'index',
        check_str=base.RULE_DEFAULT,
        description="Get all share network subnets.",
        operations=[
            {
                'method': 'GET',
                'path': '/share-networks/{share_network_id}/subnets'
            }
        ]),
]


def list_rules():
    return share_network_subnet_policies
