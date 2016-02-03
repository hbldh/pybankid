#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Release data for the PyBankID project."""

# A quick and dirty fix for installations on Heroku.
try:
    from .client import BankIDClient
    import bankid.exceptions as exceptions
    from .testcert import create_bankid_test_server_cert_and_key

    __all__ = ['BankIDClient', 'exceptions', 'create_bankid_test_server_cert_and_key', 'version']
except ImportError:
    pass

# Name of the package for release purposes.  This is the name which labels
# the tarballs and RPMs made by distutils, so it's best to lowercase it.
_name = 'pybankid'

# Version information.  An empty _version_extra corresponds to a full
# release.  'dev' as a _version_extra string means this is a development
# version.
_version_major = 0
_version_minor = 3
_version_patch = 1
# _version_extra = 'dev4'
#_version_extra = 'rc1'
_version_extra = ''  # Uncomment this for full releases

# Construct full version string from these.
_ver = [_version_major, _version_minor, _version_patch]

__version__ = '.'.join(map(str, _ver))
if _version_extra:
    __version__ = __version__ + '.' + str(_version_extra)

version = __version__  # backwards compatibility name
version_info = (_version_major, _version_minor, _version_patch, _version_extra)

_description = "BankID client for Python"

_long_description = """
PyBankID is a client for performing BankID signing.

The Swedish BankID solution for digital signing uses a SOAP
connection solution, and this module aims at providing a simplifying
client for making authentication, signing and collect requests to
the BankID servers.

The latest development version is available at the project's `GitHub
site <https://github.com/hbldh/pybankid/>`_.
"""

__license__ = 'MIT'

_authors = {
    'hbldh': ('Henrik Blidh', 'henrik.blidh@nedomkull.com'),
}
_author = 'Henrik Blidh'
_author_email = 'henrik.blidh@nedomkull.com'
_url = 'https://github.com/hbldh/pybankid/'
_download_url = 'https://github.com/hbldh/pybankid/tarball/' + '.'.join(map(str, _ver))

_platforms = ['Linux', 'Mac OSX', 'Windows XP/Vista/7/8']
_keywords = ['BankID', 'SOAP']
_classifiers = [
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS :: MacOS X',
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Security',
    'Topic :: Utilities',
]
