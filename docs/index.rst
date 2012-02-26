pyramid_ldap
============

Overview
--------

:mod:`pyramid_ldap` provides LDAP authentication services to your Pyramid
application.

.. warning:: This package only works with Pyramid 1.3a9 and better.

Installation
------------

``pyramid_ldap`` depends on the `python-ldap <http://www.python-ldap.org/>`
and `ldappool <https://github.com/mozilla-services/ldappool>`_ packages.
``python_ldap`` requires OpenLDAP development libraries to be installed
before it can successfully be installed.  An easy way to get these installed
on a Debian Linux system is to use ``apt-get build-dep python-ldap``.

After you've got the OpenLDAP dependencies installed, you can install
``pyramid_ldap`` using setuptools, e.g. (within a virtualenv)::

  $ easy_install pyramid_ldap

Setup
-----

Once :mod:`pyramid_ldap` is installed, you must use the ``config.include``
mechanism to include it into your Pyramid project's configuration.  In your
Pyramid project's ``__init__.py``:

.. code-block:: python

   config = Configurator(.....)
   config.include('pyramid_ldap')

Alternately, instead of using the Configurator's ``include`` method, you can
activate Pyramid by changing your application's ``.ini`` file, use the
following line:

.. code-block:: ini

   pyramid.includes = pyramid_ldap

Once you've included ``pyramid_ldap``, you have to call methods of the
Configurator to tell it about your LDAP server and query particulars.  Here's
an example of calling methods to create a fully-configured LDAP setup that
attempts to talk to an Active Directory server:

.. code-block:: python

    import ldap

    config = Configurator()

    config.include('pyramid_ldap')

    config.ldap_setup(
        'ldap://ldap.example.com',
        bind='CN=ldap user,CN=Users,DC=example,DC=com',
        passwd='ld@pu5er'
        )

    config.ldap_set_login_query(
        base_dn='CN=Users,DC=example,DC=com',
        filter_tmpl='(sAMAccountName=%(login)s)',
        scope = ldap.SCOPE_ONELEVEL,
        )

    config.ldap_set_groups_query(
        base_dn='CN=Users,DC=example,DC=com',
        filter_tmpl='(&(objectCategory=group)(member=%(dn)s))',
        scope = ldap.SCOPE_SUBTREE,
        cache_secs = 600,
        )

Configurator Methods
--------------------

Configuration of ``pyramid_ldap`` is done via the Configurator methods named
``ldap_setup``, ``ldap_set_login_query``, and ``ldap_set_groups_query``.  All
three of these methods should be called once (and, ideally, only once) during
the startup phase of your Pyramid application.

``Configurator.ldap_setup``

   This Configurator method accepts arguments used to set up an LDAP
   connection.  After you call it, you will be able to use the
   :func:`pyramid_ldap.get_ldap_connector` API from within your application.
   It will return a :class:`pyramid_ldap.Connector` instance.  See
   :func:`pyramid_ldap.ldap_setup` for argument details.

``Configurator.ldap_set_login_query``

   This configurator method accepts parameters which tell ``pyramid_ldap``
   how to find a user based on a login.  Invoking this method allows the LDAP
   connector's ``authenticate`` method to work.  See
   :func:`pyramid_ldap.ldap_set_login_query` for argument details.

   If ``ldap_set_login_query`` is not called, the
   :meth:`pyramid_ldap.Connector.authenticate` method will not work.

``Configurator.ldap_set_groups_query``

   This configurator method accepts parameters which tell ``pyramid_ldap``
   how to find groups based on a user DN.  Invoking this method allows the
   connector's ``user_groups`` method to work.  See
   :func:`pyramid_ldap.ldap_set_groups_query` for argument details.

   If ``ldap_set_groups_query`` is not called, the
   :meth:`pyramid_ldap.Connector.user_groups` method will not work.

Usage
-----

See the ``sampleapp`` sample application in this package for usage
information.

XXX need much more.

Logging
-------

``pyramid_ldap`` uses the logger named ``pyramid_ldap``.  It sends output at
a DEBUG level useful for its own developers to see what's happening.

More Information
----------------

.. toctree::
   :maxdepth: 1

   api.rst

Reporting Bugs / Development Versions
-------------------------------------

Visit http://github.com/Pylons/pyramid_ldap to download development or
tagged versions.

Visit http://github.com/Pylons/pyramid_ldap/issues to report bugs.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
