# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
Handles all requests to Glance.
"""

from glanceclient import client as glance_client
from glanceclient import exc as glance_exception
from keystoneauth1 import loading as ks_loading
from oslo_config import cfg

from manila.common import client_auth
from manila.common.config import core_opts
from manila.db import base

GLANCE_GROUP = 'glance'
AUTH_OBJ = None


glance_opts = [
    cfg.StrOpt('api_microversion',
               default='2',
               help='Version of Glance API to be used.'),
    cfg.StrOpt('region_name',
               default='RegionOne',
               help='Region name for connecting to glance.'),
    ]

CONF = cfg.CONF
CONF.register_opts(core_opts)
CONF.register_opts(glance_opts, GLANCE_GROUP)
ks_loading.register_session_conf_options(CONF, GLANCE_GROUP)
ks_loading.register_auth_conf_options(CONF, GLANCE_GROUP)


def list_opts():
    return client_auth.AuthClientLoader.list_opts(GLANCE_GROUP)


def glanceclient(context):
    global AUTH_OBJ
    if not AUTH_OBJ:
        AUTH_OBJ = client_auth.AuthClientLoader(
            client_class=glance_client.Client,
            exception_module=glance_exception,
            cfg_group=GLANCE_GROUP)
    return AUTH_OBJ.get_client(context,
                               version=CONF[GLANCE_GROUP].api_microversion,
                               region_name=CONF[GLANCE_GROUP].region_name)


class API(base.Base):
    """API for interacting with glanceclient."""

    def image_list(self, context):
        client = glanceclient(context)
        if hasattr(client, 'images'):
            return client.images.list()
        return client.glance.list()
