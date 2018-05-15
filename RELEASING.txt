Distributing a new release
==========================

- For clarity, we define releases as follows.

  - Alpha, beta, dev and similar statuses do not qualify whether a release is
    major or minor. The term "pre-release" means alpha, beta, or dev.

  - A release is final when it is no longer pre-release.

  - A *major* release is where the first number either before or after the
    first dot increases. Examples: 0.9.0 to 2.0.

  - A *minor* or *bug fix* release is where the number after the second dot
    increases. Example: 2.0 to 2.0.1.

Prepare new release branch
--------------------------

- On master branch:

  $ git pull

- Do platform test via tox:

- Make sure your Python has ``setuptools-git``, ``twine``, and ``wheel``
  installed:

    $ $VENV/bin/pip install setuptools-git twine wheel

- Do a platform test:

    $ tox -r

- Ensure all features of the release are documented (audit CHANGES.txt or
  communicate with contributors).

- Change CHANGES.txt heading to reflect the new version number.

- Update README.rst to use correct versions of badges and URLs according to
  each branch and context, i.e., RTD "latest" == GitHub/Travis "2.0-branch".

- For major version releases, in docs/conf.py, update values for version.

- Change setup.py version to the release version number.

- Make sure PyPI long description renders (requires ``collective.dist``
  installed into your Python)::

    $ $VENV/bin/python setup.py check -r

- Build an sdist and a wheel:

    $ $VENV/bin/python setup.py sdist bdist_wheel

- Release the wheels to PyPI:

    $ $VENV/bin/twine upload dist/pyramid_ldap-X.Y*

- Upload a git tag for the release:

    $ git tag X.Y
    $ git push origin X.Y

- Update RTD to render a new version of the docs at that tag X.Y and set X.Y
  as the default branch such that /latest/ points to it.

- Publish new version of docs.

- Announce to Twitter.

```
pyramid_ldap X.Y released.

PyPI
https://pypi.python.org/pypi/pyramid_ldap/

=== One time only for new version, first pre-release ===

Changes: http://docs.pylonsproject.org/projects/pyramid_ldap/latest/

=== For all subsequent pre-releases ===

Changes: http://docs.pylonsproject.org/projects/pyramid_ldap/latest/changes.html

Issues: https://github.com/Pylons/pyramid_ldap/issues
```

- Announce to Pyramid maillist.

```
pyramid_ldap X.Y has been released.

Here are the changes:

<<changes>>

Links

- Documentation http://docs.pylonsproject.org/projects/pyramid_ldap/latest/#changelog

- Github https://github.com/pylons/pyramid_ldap/

- PyPi https://pypi.python.org/pypi/pyramid_ldap/

Enjoy, and please report any issues you find to the issue tracker at
https://github.com/Pylons/pyramid_ldap/issues

Thanks!

- pyramid_ldap developers
```
