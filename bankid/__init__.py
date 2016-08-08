#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Release data for the PyBankID project."""

# A quick and dirty fix for installation and importing.
try:
    from .client import BankIDClient
    import bankid.exceptions as exceptions
    from .certutils import create_bankid_test_server_cert_and_key

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
_version_patch = 6
# _version_extra = 'dev1'
# _version_extra = 'a1'
_version_extra = ''  # Uncomment this for full releases

# Construct full version string from these.
_ver = [_version_major, _version_minor, _version_patch]

__version__ = '.'.join(map(str, _ver))
if _version_extra:
    __version__ = __version__ + '.' + str(_version_extra)

version = __version__  # backwards compatibility name
version_info = (_version_major, _version_minor, _version_patch, _version_extra)

__description__ = "BankID client for Python"

__license__ = 'MIT'

__authors__ = {
    'hbldh': ('Henrik Blidh', 'henrik.blidh@nedomkull.com'),
}
__author__ = 'Henrik Blidh'
__author_email__ = 'henrik.blidh@nedomkull.com'
__url__ = 'https://github.com/hbldh/pybankid/'
__download_url__ = 'https://github.com/hbldh/pybankid/tarball/' + '.'.join(map(str, _ver))

__platforms__ = ['Linux', 'Mac OSX', 'Windows XP/Vista/7/8']
__keywords__ = ['BankID', 'SOAP']
__classifiers__ = [
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
