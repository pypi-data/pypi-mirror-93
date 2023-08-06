.. _configuration-bifrost:

=======
Bifrost
=======

This section covers configuration of the Bifrost service that runs on the seed
host. Bifrost configuration is typically applied in
``${KAYOBE_CONFIG_PATH}/bifrost.yml``. Consult the :bifrost-doc:`Bifrost
documentation <>` for further details of Bifrost usage and configuration.

Bifrost installation
====================

.. note::

   This section may be skipped if using an upstream Bifrost container image.

The following options are used if building the Bifrost container image locally.

``kolla_bifrost_source_url``
    URL of Bifrost source code repository.  Default is
    https://opendev.org/openstack/bifrost.
``kolla_bifrost_source_version``
    Version (branch, tag, etc.) of Bifrost source code repository. Default is
    ``{{ openstack_branch }}``, which is the same as the Kayobe upstream branch
    name.

For example, to install Bifrost from a custom git repository:

.. code-block:: yaml
   :caption: ``bifrost.yml``

   kolla_bifrost_source_url: https://git.example.com/bifrost
   kolla_bifrost_source_version: downstream

.. _configuration-bifrost-overcloud-root-image:

Overcloud root disk image configuration
=======================================

Bifrost uses Diskimage builder (DIB) to build a root disk image that is
deployed to overcloud hosts when they are provisioned. The following options
configure how this image is built.  Consult the
:diskimage-builder-doc:`Diskimage-builder documentation <>` for further
information on building disk images.

The default configuration builds a CentOS 7 whole disk (partitioned) image with
SELinux disabled and a serial console enabled. `Cloud-init
<https://cloudinit.readthedocs.io/en/latest/>`__ is used to process the
configuration drive built by Bifrost, rather than the Bifrost default of
:diskimage-builder-doc:`simple-init <elements/simple-init/README>`.

``kolla_bifrost_dib_os_element``
    DIB base OS element. Default is ``centos7``.
``kolla_bifrost_dib_os_release``
    DIB image OS release. Default is ``GenericCloud``.
``kolla_bifrost_dib_elements_default``
    *Added in the Train release. Use kolla_bifrost_dib_elements in earlier
    releases.*

    List of default DIB elements. Default is ``["disable-selinux",
    "enable-serial-console", "vm"]``. The ``vm`` element is poorly named, and
    causes DIB to build a whole disk image rather than a single partition.
``kolla_bifrost_dib_elements_extra``
    *Added in the Train release. Use kolla_bifrost_dib_elements in earlier
    releases.*

    List of additional DIB elements. Default is none.
``kolla_bifrost_dib_elements``
    List of DIB elements. Default is a combination of
    ``kolla_bifrost_dib_elements_default`` and
    ``kolla_bifrost_dib_elements_extra``.
``kolla_bifrost_dib_init_element``
    DIB init element. Default is ``cloud-init-datasources``.
``kolla_bifrost_dib_env_vars_default``
    *Added in the Train release. Use kolla_bifrost_dib_env_vars in earlier
    releases.*

    DIB default environment variables. Default is
    ``{"DIB_CLOUD_INIT_DATASOURCES": "ConfigDrive"}``.
``kolla_bifrost_dib_env_vars_extra``
    *Added in the Train release. Use kolla_bifrost_dib_env_vars in earlier
    releases.*

    DIB additional environment variables. Default is none.
``kolla_bifrost_dib_env_vars``
    DIB environment variables. Default is combination of
    ``kolla_bifrost_dib_env_vars_default`` and
    ``kolla_bifrost_dib_env_vars_extra``.
``kolla_bifrost_dib_packages``
    List of DIB packages to install. Default is to install no extra packages.

The disk image is built during the deployment of seed services. It is worth
noting that currently, the image will not be rebuilt if it already exists. To
force rebuilding the image, it is necessary to remove the file. On the seed:

.. code-block:: console

   docker exec bifrost_deploy rm /httpboot/deployment_image.qcow2

Then on the control host:

.. code-block:: console

   (kayobe) $ kayobe seed service deploy

Example: Adding an element
--------------------------

In the following, we extend the list of DIB elements to add the ``growpart``
element:

.. code-block:: yaml
   :caption: ``bifrost.yml``

   kolla_bifrost_dib_elements_extra:
     - "growpart"

Example: Building an XFS root filesystem image
----------------------------------------------

By default, DIB will format the image as ``ext4``. In some cases it might be
useful to use XFS, for example when using the ``overlay`` Docker storage driver
which can reach the maximum number of hardlinks allowed by ``ext4``.

In DIB, we achieve this by setting the ``FS_TYPE`` environment variable to
``xfs``.

.. code-block:: yaml
   :caption: ``bifrost.yml``

   kolla_bifrost_dib_env_vars_extra:
     FS_TYPE: "xfs"

In order to build the image, we also require the ``xfsprogs`` package
to be installed in the Bifrost container. As of the Ussuri release of Bifrost
this will be done automatically, but until then, the following workaround
can be made on the seed host:

.. code-block:: console

   docker exec bifrost_deploy yum -y install xfsprogs

Example: Configuring a development user account
-----------------------------------------------

.. warning::

   A development user account should not be used in production.

When debugging a failed deployment, it can sometimes be necessary to allow
access to the image via a preconfigured user account with a known password.
This can be achieved via the :diskimage-builder-doc:`devuser
<elements/devuser/README>` element.

This example shows how to add the ``devuser`` element, and configure a username
and password for an account that has passwordless sudo:

.. code-block:: yaml
   :caption: ``bifrost.yml``

   kolla_bifrost_dib_elements_extra:
     - "devuser"

   kolla_bifrost_dib_env_vars_extra:
     DIB_DEV_USER_USERNAME: "devuser"
     DIB_DEV_USER_PASSWORD: "correct horse battery staple"
     DIB_DEV_USER_PWDLESS_SUDO: "yes"

Alternatively, the :diskimage-builder-doc:`dynamic-login element
<elements/dynamic-login/README>` can be used to authorize SSH keys by appending
them to the kernel arguments.

Example: Installing a package
-----------------------------

It can be necessary to install additional packages in the root disk image.
Rather than needing to write a custom DIB element, we can use the
``kolla_bifrost_dib_packages`` variable. For example, to install the
``biosdevname`` package:

.. code-block:: yaml
   :caption: ``ipa.yml``

   kolla_bifrost_dib_packages:
     - "biosdevname"

Ironic configuration
====================

The following options configure the Ironic service in the ``bifrost-deploy``
container.

``kolla_bifrost_enabled_hardware_types``
    List of :ironic-doc:`hardware types <admin/drivers>` to enable for
    Bifrost's Ironic. Default is ``["ipmi"]``.

Ironic Inspector configuration
==============================

The following options configure the Ironic Inspector service in the
``bifrost-deploy`` container.

``kolla_bifrost_inspector_processing_hooks``
    List of of inspector processing plugins. Default is ``{{
    inspector_processing_hooks }}``, defined in
    ``${KAYOBE_CONFIG_PATH}/inspector.yml``.
``kolla_bifrost_inspector_port_addition``
    Which MAC addresses to add as ports during introspection. One of ``all``,
    ``active`` or ``pxe``. Default is ``{{ inspector_add_ports }}``, defined in
    ``${KAYOBE_CONFIG_PATH}/inspector.yml``.
``kolla_bifrost_inspector_extra_kernel_options``
    List of extra kernel parameters for the inspector default PXE
    configuration. Default is ``{{ inspector_extra_kernel_options }}``, defined
    in ``${KAYOBE_CONFIG_PATH}/inspector.yml``.
``kolla_bifrost_inspector_rules``
    List of introspection rules for Bifrost's Ironic Inspector service. Default
    is ``{{ inspector_rules }}``, defined in
    ``${KAYOBE_CONFIG_PATH}/inspector.yml``.
``kolla_bifrost_inspector_ipmi_username``
    Ironic inspector IPMI username to set via an introspection rule. Default is
    ``{{ ipmi_username }}``, defined in ``${KAYOBE_CONFIG_PATH}/bmc.yml``.
``kolla_bifrost_inspector_ipmi_password``
    Ironic inspector IPMI password to set via an introspection rule. Default is
    ``{{ ipmi_password }}``, defined in ``${KAYOBE_CONFIG_PATH}/bmc.yml``.
``kolla_bifrost_inspector_lldp_switch_port_interface``
    Ironic inspector network interface name on which to check for an LLDP switch
    port description to use as the node's name. Default is ``{{
    inspector_lldp_switch_port_interface_default }}``, defined in
    ``${KAYOBE_CONFIG_PATH}/inspector.yml``.
``kolla_bifrost_inspector_deploy_kernel``
    Ironic inspector deployment kernel location. Default is ``http://{{
    provision_oc_net_name | net_ip }}:8080/ipa.vmlinuz``.
``kolla_bifrost_inspector_deploy_ramdisk``
    Ironic inspector deployment ramdisk location. Default is ``http://{{
    provision_oc_net_name | net_ip }}:8080/ipa.initramfs``.

Ironic Python Agent (IPA) configuration
=======================================

.. note::

   If building IPA images locally (``ipa_build_images`` is ``true``) this
   section can be skipped.

The following options configure the source of Ironic Python Agent images used
by Bifrost for inspection and deployment.  Consult the
:ironic-python-agent-doc:`Ironic Python Agent documentation <>` for full
details.

``kolla_bifrost_ipa_kernel_upstream_url``
    URL of Ironic Python Agent (IPA) kernel image. Default is ``{{
    inspector_ipa_kernel_upstream_url }}``, defined in
    ``${KAYOBE_CONFIG_PATH}/inspector.yml``.
``kolla_bifrost_ipa_kernel_checksum_url``
    URL of checksum of Ironic Python Agent (IPA) kernel image. Default is ``{{
    inspector_ipa_kernel_checksum_url }}``, defined in
    ``${KAYOBE_CONFIG_PATH}/inspector.yml``.
``kolla_bifrost_ipa_kernel_checksum_algorithm``
    Algorithm of checksum of Ironic Python Agent (IPA) kernel image. Default is
    ``{{ inspector_ipa_kernel_checksum_algorithm }}``, defined in
    ``${KAYOBE_CONFIG_PATH}/inspector.yml``.
``kolla_bifrost_ipa_ramdisk_upstream_url``
    URL of Ironic Python Agent (IPA) ramdisk image. Default is ``{{
    inspector_ipa_ramdisk_upstream_url }}``, defined in
    ``${KAYOBE_CONFIG_PATH}/inspector.yml``.
``kolla_bifrost_ipa_ramdisk_checksum_url``
    URL of checksum of Ironic Python Agent (IPA) ramdisk image. Default is ``{{
    inspector_ipa_ramdisk_checksum_url }}``, defined in
    ``${KAYOBE_CONFIG_PATH}/inspector.yml``.
``kolla_bifrost_ipa_ramdisk_checksum_algorithm``
    Algorithm of checksum of Ironic Python Agent (IPA) ramdisk image. Default
    is ``{{ inspector_ipa_ramdisk_checksum_algorithm }}``, defined in
    ``${KAYOBE_CONFIG_PATH}/inspector.yml``.

Inventory configuration
=======================

.. note::

   This feature is currently not well tested. It is advisable to use
   autodiscovery of overcloud servers instead.

The following options are used to configure a static inventory of servers for
Bifrost.

``kolla_bifrost_servers``

    Server inventory for Bifrost in the :bifrost-doc:`JSON file format
    <user/howto#json-file-format>`.

Custom Configuration
====================

Further configuration of arbitrary Ansible variables for Bifrost can be
provided via the following files:

* ``${KAYOBE_CONFIG_PATH}/kolla/config/bifrost/bifrost.yml``
* ``${KAYOBE_CONFIG_PATH}/kolla/config/bifrost/dib.yml``

These are both passed as extra variables files to ``ansible-playbook``, but the
naming scheme provides a separation of DIB image related variables from other
variables. It may be necessary to inspect the `Bifrost source code
<https://opendev.org/openstack/bifrost>`__ for the full set of variables that
may be configured.

For example, to configure debug logging for Ironic Inspector:

.. code-block:: yaml
   :caption: ``kolla/config/bifrost/bifrost.yml``

   inspector_debug: true
