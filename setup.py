import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid>=1.3a9',
    'ldappool',
    'python-ldap',
    ]

sampleapp_requires = [
    'waitress',
    'pyramid_debugtoolbar',
    ]

setup(name='pyramid_ldap',
      version='0.0',
      description='pyramid_ldap',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP",
        ],
      author='Chris McDonough',
      author_email='pylons-discuss@groups.google.com',
      url='http://pylonsproject.org',
      keywords='web pyramid pylons ldap',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      extras_require = {'sampleapp':sampleapp_requires},
      test_suite="pyramid_ldap",
      entry_points = """\
      [paste.app_factory]
      sampleapp = sampleapp:main
      """,
      )

