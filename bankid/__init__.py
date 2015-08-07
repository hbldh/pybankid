#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Release data for the PyBankID project."""

# Name of the package for release purposes.  This is the name which labels
# the tarballs and RPMs made by distutils, so it's best to lowercase it.
name = 'pybankid'

# Version information.  An empty _version_extra corresponds to a full
# release.  'dev' as a _version_extra string means this is a development
# version.
_version_major = 0
_version_minor = 1
_version_patch = 4
#_version_extra = 'dev4'
#_version_extra = 'b1'
_version_extra = ''  # Uncomment this for full releases

# Construct full version string from these.
_ver = [_version_major, _version_minor, _version_patch]

__version__ = '.'.join(map(str, _ver))
if _version_extra:
    __version__ = __version__ + '.' + str(_version_extra)

version = __version__  # backwards compatibility name
version_info = (_version_major, _version_minor, _version_patch, _version_extra)

description = "BankID client for Python"

long_description = \
"""PyBankID is a client for performing BankID signing.

The Swedish BankID solution for digital signing uses a SOAP
connection solution, and this module aims at providing a simplifying
client for making authentication, signing and collect requests to
the BankID servers.

The latest development version is available at the project's `GitHub
site <https://github.com/hbldh/pybankid/>`_.

"""

license = 'MIT'

authors = {'hbldh': ('Henrik Blidh', 'henrik.blidh@nedomkull.com'),
           }
author = 'Henrik Blidh'
author_email = 'henrik.blidh@nedomkull.com'
url = 'https://github.com/hbldh/pybankid/'
download_url = 'https://github.com/hbldh/pybankid/downloads'

platforms = ['Linux', 'Mac OSX', 'Windows XP/Vista/7/8']
keywords = ['BankID', 'SOAP']
classifiers = [
    'Programming Language :: Python :: 2.7',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS :: MacOS X',
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Utilities'
    ]
