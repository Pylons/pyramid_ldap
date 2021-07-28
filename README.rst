############
Pyramid LDAP
############
# Need to update to latest python version

``pyramid_ldap`` provides LDAP authentication services for your Pyramid
application.  Thanks to the ever-awesome `SurveyMonkey
<http://surveymonkey.com>`_ for sponsoring the development of this package!

See the documentation at
https://docs.pylonsproject.org/projects/pyramid_ldap/en/latest/ for more
information.

This package will only work with Pyramid 1.3 and later.

Installation
------------

``pyramid_ldap`` uses ``pyldap`` which in turn requires ``libldap2`` and
``libsasl2`` development headers installed.

On Ubuntu 16.04 you can install them using the command ``apt-get install libldap2-dev libsasl2-dev``.

