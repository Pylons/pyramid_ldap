import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.rst')) as f:
        README = f.read()
    with open(os.path.join(here, 'CHANGES.txt')) as f:
        CHANGES = f.read()
except IOError:
    README = CHANGES = ''

requires = [
    'pyramid>=1.3',
    'six',
    ]
if 'READTHEDOCS' not in os.environ:
    # hail mary for readthedocs
    requires.extend(['ldappool', 'python-ldap'])

sampleapp_extras = [
    'waitress',
    'pyramid_debugtoolbar',
    ]
testing_extras = ['nose', 'coverage']
docs_extras = ['Sphinx >= 1.7.4']

setup(name='pyramid_ldap',
      version='0.2',
      description='pyramid_ldap',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP",
        "License :: Repoze Public License",
      ],
      author='Chris McDonough',
      author_email='pylons-discuss@groups.google.com',
      url='https://pylonsproject.org',
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      keywords='web pyramid pylons ldap',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      extras_require={
          'sampleapp': sampleapp_extras,
          'docs': docs_extras,
          'testing': testing_extras,
          },
      test_suite="pyramid_ldap",
      entry_points="""\
          [paste.app_factory]
          sampleapp = sampleapp:main
      """,
      )
