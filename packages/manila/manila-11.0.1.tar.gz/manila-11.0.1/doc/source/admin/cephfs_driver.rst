..
      Copyright 2016 Red Hat, Inc.
      All Rights Reserved.

      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

=============
CephFS driver
=============

The CephFS driver enables manila to export shared filesystems backed by Ceph's
File System (CephFS) using either the Ceph network protocol or NFS protocol.
Guests require a native Ceph client or an NFS client in order to mount the
filesystem.

When guests access CephFS using the native Ceph protocol, access is
controlled via Ceph's cephx authentication system. If a user requests
share access for an ID, Ceph creates a corresponding Ceph auth ID and a secret
key if they do not already exist, and authorizes the ID to access the share.
The client can then mount the share using the ID and the secret key. To learn
more about configuring Ceph clients to access the shares created using this
driver, please see the `Ceph documentation`_

And when guests access CephFS through NFS, an NFS-Ganesha server mediates
access to CephFS. The driver enables access control by managing the NFS-Ganesha
server's exports.


Supported Operations
~~~~~~~~~~~~~~~~~~~~

The following operations are supported with CephFS backend:

- Create/delete share
- Allow/deny access to share

  * Only ``cephx`` access type is supported for CephFS native protocol.
  * Only ``ip`` access type is supported for NFS protocol.
  * ``read-only`` and ``read-write`` access levels are supported.

- Extend/shrink share
- Create/delete snapshot
- Create/delete share groups
- Create/delete share group snapshots


Prerequisites
~~~~~~~~~~~~~

.. important:: A manila share backed by CephFS is only as good as the
               underlying filesystem. Take care when configuring your Ceph
               cluster, and consult the latest guidance on the use of
               CephFS in the `Ceph documentation`_.



Ceph testing matrix
-------------------

As Ceph and Manila continue to grow, it is essential to test and support
combinations of releases supported by both projects. However, there is
little community bandwidth to cover all of them. Below is the current state of
testing for Ceph releases with this project. Adjacent components such as
`devstack-plugin-ceph <https://opendev.org/openstack/devstack-plugin-ceph>`_
and `tripleo <https://opendev.org/openstack/tripleo-heat-templates>`_ are
added to the table below. Contributors to those projects can determine what
versions of ceph are tested and supported with manila by those components;
however, their state is presented here for ease of access.

.. important::

    From the Victoria cycle, the Manila CephFS driver is not tested or
    supported with Ceph clusters older than Nautilus. Future releases of
    Manila may be incompatible with Nautilus too! We suggest always running
    the latest version of Manila with the latest release of Ceph.

+-------------------+----------+----------------------+-----------+
| OpenStack release |  manila  | devstack-plugin-ceph | tripleo   |
+===================+==========+======================+===========+
| Queens            | Luminous | Luminous             | Luminous  |
+-------------------+----------+----------------------+-----------+
| Rocky             | Luminous | Luminous             | Luminous  |
+-------------------+----------+----------------------+-----------+
| Stein             | Nautilus | Luminous, Nautilus   | Nautilus  |
+-------------------+----------+----------------------+-----------+
| Train             | Nautilus | Luminous, Nautilus   | Nautilus  |
+-------------------+----------+----------------------+-----------+
| Ussuri            | Nautilus | Luminous, Nautilus   | Nautilus  |
+-------------------+----------+----------------------+-----------+
| Victoria          | Nautilus | Nautilus             | Nautilus  |
+-------------------+----------+----------------------+-----------+


Common Prerequisites
--------------------

- A Ceph cluster with a filesystem configured (See `Create ceph filesystem`_ on
  how to create a filesystem.)
- ``ceph-common`` package installed in the servers running the
  :term:`manila-share` service.
- Network connectivity between your Ceph cluster's public network and the
  servers running the :term:`manila-share` service.

For CephFS native shares
------------------------
- Ceph client installed in the guest
- Network connectivity between your Ceph cluster's public network and guests.
  See :ref:`security_cephfs_native`.

For CephFS NFS shares
---------------------

- 2.5 or later versions of NFS-Ganesha.
- NFS client installed in the guest.
- Network connectivity between your Ceph cluster's public network and
  NFS-Ganesha server.
- Network connectivity between your NFS-Ganesha server and the manila
  guest.

.. _authorize_ceph_driver:

Authorizing the driver to communicate with Ceph
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the following commands to create a Ceph identity for a driver instance
to use:

.. code-block:: console

    read -d '' MON_CAPS << EOF
    allow r,
    allow command "auth del",
    allow command "auth caps",
    allow command "auth get",
    allow command "auth get-or-create"
    EOF

    ceph auth get-or-create client.manila -o manila.keyring \
    mds 'allow *' \
    osd 'allow rw' \
    mon "$MON_CAPS"


``manila.keyring``, along with your ``ceph.conf`` file, will then need to be
placed on the server running the :term:`manila-share` service.

.. important::

    To communicate with the Ceph backend, a CephFS driver instance
    (represented as a backend driver section in manila.conf) requires its own
    Ceph auth ID that is not used by other CephFS driver instances running in
    the same controller node.

In the server running the :term:`manila-share` service, you can place the
``ceph.conf`` and ``manila.keyring`` files in the /etc/ceph directory. Set the
same owner for the :term:`manila-share` process and the ``manila.keyring``
file. Add the following section to the ``ceph.conf`` file.

.. code-block:: ini

    [client.manila]
    client mount uid = 0
    client mount gid = 0
    log file = /opt/stack/logs/ceph-client.manila.log
    admin socket = /opt/stack/status/stack/ceph-$name.$pid.asok
    keyring = /etc/ceph/manila.keyring

It is advisable to modify the Ceph client's admin socket file and log file
locations so that they are co-located with manila services's pid files and
log files respectively.


Enabling snapshot support in Ceph backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CephFS Snapshots were experimental prior to the Nautilus release of Ceph.
There may be some `limitations on snapshots`_ based on the Ceph version you
use.

From Ceph Nautilus, all new filesystems created on Ceph have snapshots
enabled by default. If you've upgraded your ceph cluster and want to enable
snapshots on a pre-existing filesystem, you can do so:

.. code-block:: console

    ceph fs set {fs_name} allow_new_snaps true

Configuring CephFS backend in manila.conf
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure CephFS native share backend in manila.conf
----------------------------------------------------

Add CephFS to ``enabled_share_protocols`` (enforced at manila api layer). In
this example we leave NFS and CIFS enabled, although you can remove these
if you will only use a CephFS backend:

.. code-block:: ini

    enabled_share_protocols = NFS,CIFS,CEPHFS

Create a section like this to define a CephFS native backend:

.. code-block:: ini

    [cephfsnative1]
    driver_handles_share_servers = False
    share_backend_name = CEPHFSNATIVE1
    share_driver = manila.share.drivers.cephfs.driver.CephFSDriver
    cephfs_conf_path = /etc/ceph/ceph.conf
    cephfs_protocol_helper_type = CEPHFS
    cephfs_auth_id = manila
    cephfs_cluster_name = ceph

Set ``driver-handles-share-servers`` to ``False`` as the driver does not
manage the lifecycle of ``share-servers``. For the driver backend to expose
shares via the native Ceph protocol, set ``cephfs_protocol_helper_type`` to
``CEPHFS``.

Then edit ``enabled_share_backends`` to point to the driver's backend section
using the section name. In this example we are also including another backend
("generic1"), you would include whatever other backends you have configured.


.. code-block:: ini

    enabled_share_backends = generic1, cephfsnative1


Configure CephFS NFS share backend in manila.conf
-------------------------------------------------

.. note::

    Prior to configuring the Manila CephFS driver to use NFS, you must have
    installed and configured NFS-Ganesha. For guidance on configuration,
    refer to the `NFS-Ganesha setup guide
    <../contributor/ganesha.html#nfs-ganesha-configuration>`_.

Add NFS to ``enabled_share_protocols`` if it's not already there:

.. code-block:: ini

    enabled_share_protocols = NFS,CIFS,CEPHFS


Create a section to define a CephFS NFS share backend:

.. code-block:: ini

    [cephfsnfs1]
    driver_handles_share_servers = False
    share_backend_name = CEPHFSNFS1
    share_driver = manila.share.drivers.cephfs.driver.CephFSDriver
    cephfs_protocol_helper_type = NFS
    cephfs_conf_path = /etc/ceph/ceph.conf
    cephfs_auth_id = manila
    cephfs_cluster_name = ceph
    cephfs_ganesha_server_is_remote= False
    cephfs_ganesha_server_ip = 172.24.4.3
    ganesha_rados_store_enable = True
    ganesha_rados_store_pool_name = cephfs_data


The following options are set in the driver backend section above:

* ``driver-handles-share-servers`` to ``False`` as the driver does not
  manage the lifecycle of ``share-servers``.

* ``cephfs_protocol_helper_type`` to ``NFS`` to allow NFS protocol access to
  the CephFS backed shares.

* ``ceph_auth_id`` to the ceph auth ID created in :ref:`authorize_ceph_driver`.

* ``cephfs_ganesha_server_is_remote`` to False if the NFS-ganesha server is
  co-located with the :term:`manila-share`  service. If the NFS-Ganesha
  server is remote, then set the options to ``True``, and set other options
  such as ``cephfs_ganesha_server_ip``, ``cephfs_ganesha_server_username``,
  and ``cephfs_ganesha_server_password`` (or ``cephfs_ganesha_path_to_private_key``)
  to allow the driver to manage the NFS-Ganesha export entries over SSH.

* ``cephfs_ganesha_server_ip`` to the ganesha server IP address. It is
  recommended to set this option even if the ganesha server is co-located
  with the :term:`manila-share` service.

* ``ganesha_rados_store_enable`` to True or False. Setting this option to
  True allows NFS Ganesha to store exports and its export counter in Ceph
  RADOS objects. We recommend setting this to True and using a RADOS object
  since it is useful for highly available NFS-Ganesha deployments to store
  their configuration efficiently in an already available distributed
  storage system.

* ``ganesha_rados_store_pool_name`` to the name of the RADOS pool you have
  created for use with NFS-Ganesha. Set this option only if also setting
  the ``ganesha_rados_store_enable`` option to True. If you want to use
  one of the backend CephFS's RADOS pools, then using CephFS's data pool is
  preferred over using its metadata pool.

Edit ``enabled_share_backends`` to point to the driver's backend section
using the section name, ``cephfsnfs1``.

.. code-block:: ini

    enabled_share_backends = generic1, cephfsnfs1


Space considerations
~~~~~~~~~~~~~~~~~~~~

The CephFS driver reports total and free capacity available across the Ceph
cluster to manila to allow provisioning. All CephFS shares are thinly
provisioned, i.e., empty shares do not consume any significant space
on the cluster. The CephFS driver does not allow controlling oversubscription
via manila. So, as long as there is free space, provisioning will continue,
and eventually this may cause your Ceph cluster to be over provisioned and
you may run out of space if shares are being filled to capacity. It is advised
that you use Ceph's monitoring tools to monitor space usage and add more
storage when required in order to honor space requirements for provisioned
manila shares. You may use the driver configuration option
``reserved_share_percentage`` to prevent manila from filling up your Ceph
cluster, and allow existing shares to grow.

Creating shares
~~~~~~~~~~~~~~~

Create CephFS native share
--------------------------

The default share type may have ``driver_handles_share_servers`` set to True.
Configure a share type suitable for CephFS native share:

.. code-block:: console

    manila type-create cephfsnativetype false
    manila type-key cephfsnativetype set vendor_name=Ceph storage_protocol=CEPHFS

Then create a share,

.. code-block:: console

    manila create --share-type cephfsnativetype --name cephnativeshare1 cephfs 1

Note the export location of the share:

.. code-block:: console

    manila share-export-location-list cephnativeshare1

The export location of the share contains the Ceph monitor (mon) addresses and
ports, and the path to be mounted. It is of the form,
``{mon ip addr:port}[,{mon ip addr:port}]:{path to be mounted}``

Create CephFS NFS share
-----------------------

Configure a share type suitable for CephFS NFS share:

.. code-block:: console

    manila type-create cephfsnfstype false
    manila type-key cephfsnfstype set vendor_name=Ceph storage_protocol=NFS

Then create a share:

.. code-block:: console

    manila create --share-type cephfsnfstype --name cephnfsshare1 nfs 1

Note the export location of the share:

.. code-block:: console

    manila share-export-location-list cephnfsshare1

The export location of the share contains the IP address of the NFS-Ganesha
server and the path to be mounted. It is of the form,
``{NFS-Ganesha server address}:{path to be mounted}``


Allowing access to shares
~~~~~~~~~~~~~~~~~~~~~~~~~

Allow access to CephFS native share
-----------------------------------

Allow Ceph auth ID ``alice`` access to the share using ``cephx`` access type.

.. code-block:: console

    manila access-allow cephnativeshare1 cephx alice

Note the access status, and the access/secret key of ``alice``.

.. code-block:: console

    manila access-list cephnativeshare1


Allow access to CephFS NFS share
--------------------------------

Allow a guest access to the share using ``ip`` access type.

.. code-block:: console

    manila access-allow cephnfsshare1 ip 172.24.4.225


Mounting CephFS shares
~~~~~~~~~~~~~~~~~~~~~~

Mounting CephFS native share using FUSE client
----------------------------------------------

Using the secret key of the authorized ID ``alice`` create a keyring file,
``alice.keyring`` like:

.. code-block:: ini

    [client.alice]
            key = AQA8+ANW/4ZWNRAAOtWJMFPEihBA1unFImJczA==


Using the mon IP addresses from the share's export location, create a
configuration file, ``ceph.conf`` like:

.. code-block:: ini

    [client]
            client quota = true
            mon host = 192.168.1.7:6789, 192.168.1.8:6789, 192.168.1.9:6789

Finally, mount the filesystem, substituting the filenames of the keyring and
configuration files you just created, and substituting the path to be mounted
from the share's export location:

.. code-block:: console

    sudo ceph-fuse ~/mnt \
    --id=alice \
    --conf=./ceph.conf \
    --keyring=./alice.keyring \
    --client-mountpoint=/volumes/_nogroup/4c55ad20-9c55-4a5e-9233-8ac64566b98c


Mounting CephFS native share using Kernel client
------------------------------------------------

If you have the ``ceph-common`` package installed in the client host, you can
use the kernel client to mount CephFS shares.

.. important::

    If you choose to use the kernel client rather than the FUSE client the
    share size limits set in manila may not be obeyed in versions of kernel
    older than 4.17 and Ceph versions older than mimic. See the
    `quota limitations documentation`_ to understand CephFS quotas.

The mount command is as follows:

.. code-block:: console

    mount -t ceph {mon1 ip addr}:6789,{mon2 ip addr}:6789,{mon3 ip addr}:6789:/ \
        {mount-point} -o name={access-id},secret={access-key}

With our earlier examples, this would be:

.. code-block:: console

    mount -t ceph 192.168.1.7:6789, 192.168.1.8:6789, 192.168.1.9:6789:/ \
        /volumes/_nogroup/4c55ad20-9c55-4a5e-9233-8ac64566b98c \
        -o name=alice,secret='AQA8+ANW/4ZWNRAAOtWJMFPEihBA1unFImJczA=='


Mount CephFS NFS share using NFS client
---------------------------------------

In the guest, mount the share using the NFS client and knowing the share's
export location.

.. code-block:: ini

    sudo mount -t nfs 172.24.4.3:/volumes/_nogroup/6732900b-32c1-4816-a529-4d6d3f15811e /mnt/nfs/

Known restrictions
~~~~~~~~~~~~~~~~~~

- A CephFS driver instance, represented as a backend driver section in
  manila.conf, requires a Ceph auth ID unique to the backend Ceph Filesystem.
  Using a non-unique Ceph auth ID will result in the driver unintentionally
  evicting other CephFS clients using the same Ceph auth ID to connect to the
  backend.

- Snapshots are read-only. A user can read a snapshot's contents from the
  ``.snap/{manila-snapshot-id}_{unknown-id}`` folder within the mounted
  share.


Security
~~~~~~~~

- Each share's data is mapped to a distinct Ceph RADOS namespace. A guest is
  restricted to access only that particular RADOS namespace.
  https://docs.ceph.com/docs/nautilus/cephfs/file-layouts/

- An additional level of resource isolation can be provided by mapping a
  share's contents to a separate RADOS pool. This layout would be preferred
  only for cloud deployments with a limited number of shares needing strong
  resource separation. You can do this by setting a share type specification,
  ``cephfs:data_isolated`` for the share type used by the cephfs driver.

  .. code-block:: console

    manila type-key cephfstype set cephfs:data_isolated=True

.. _security_cephfs_native:

Security with CephFS native share backend
-----------------------------------------

As the guests need direct access to Ceph's public network, CephFS native
share backend is suitable only in private clouds where guests can be trusted.

.. _Ceph documentation: https://docs.ceph.com/docs/nautilus/cephfs/
.. _Create ceph filesystem: https://docs.ceph.com/docs/nautilus/cephfs/createfs/
.. _limitations on snapshots: https://docs.ceph.com/docs/nautilus/cephfs/experimental-features/#snapshots
.. _quota limitations documentation: https://docs.ceph.com/docs/nautilus/cephfs/quota/#limitations

The :mod:`manila.share.drivers.cephfs.driver` Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: manila.share.drivers.cephfs.driver
    :noindex:
    :members:
    :undoc-members:
    :show-inheritance:
