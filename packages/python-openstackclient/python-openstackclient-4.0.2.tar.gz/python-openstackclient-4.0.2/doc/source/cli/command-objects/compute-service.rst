===============
compute service
===============

Compute v2

compute service delete
----------------------

Delete compute service(s)

.. program:: compute service delete
.. code:: bash

    openstack compute service delete
        <service> [<service> ...]

.. _compute_service_delete-service:
.. describe:: <service>

    Compute service(s) to delete (ID only). If using
    ``--os-compute-api-version`` 2.53 or greater, the ID is a UUID which can
    be retrieved by listing compute services using the same 2.53+ microversion.

compute service list
--------------------

List compute services

Using ``--os-compute-api-version`` 2.53 or greater will return the ID as a
UUID value which can be used to uniquely identify the service in a multi-cell
deployment.

.. program:: compute service list
.. code:: bash

    openstack compute service list
        [--host <host>]
        [--service <service>]
        [--long]

.. option:: --host <host>

    List services on specified host (name only)

.. option:: --service <service>

    List only specified service binaries (name only). For example,
    ``nova-compute``, ``nova-conductor``, etc.

.. option:: --long

    List additional fields in output

compute service set
-------------------

Set compute service properties

.. program:: compute service set
.. code:: bash

    openstack compute service set
        [--enable | --disable]
        [--disable-reason <reason>]
        [--up | --down]
        <host> <service>

.. option:: --enable

    Enable service

.. option:: --disable

    Disable service

.. option:: --disable-reason <reason>

    Reason for disabling the service (in quotes). Should be used with :option:`--disable` option.

.. option:: --up

    Force up service. Requires ``--os-compute-api-version`` 2.11 or greater.

.. option:: --down

    Force down service. . Requires ``--os-compute-api-version`` 2.11 or
    greater.

.. _compute_service_set-host:
.. describe:: <host>

    Name of host

.. describe:: <service>

    Name of service (Binary name), for example ``nova-compute``
