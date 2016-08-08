# -*- coding: utf-8 -*-
"""
PyBankID
========

PyBankID is a client for performing BankID signing.

The Swedish BankID solution for digital signing uses a SOAP
connection solution, and this module aims at providing a simplifying
client for making authentication, signing and collect requests to
the BankID servers.

The latest development version is available at the project's `GitHub
site <https://github.com/hbldh/pybankid/>`_.

Created by hbldh <henrik.blidh@nedomkull.com>
Created on 2013-09-14, 19:31

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
from setuptools import setup, find_packages
import bankid

# Get the long description from the README file
try:
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.rst')) as f:
        long_description = f.read()
except:
    long_description = __doc__


setup(
    name='pybankid',
    version=bankid.__version__,
    author=bankid.__author__,
    author_email=bankid.__author_email__,
    description=bankid.__description__,
    long_description=long_description,
    license=bankid.__license__,
    url=bankid.__url__,
    classifiers=bankid.__classifiers__,
    platforms=bankid.__platforms__,
    packages=find_packages(exclude=('tests', )),
    package_data={'': ['*.pem']},
    install_requires=[
        'requests>=2.7.0',
        'suds-jurko>=0.6',
        'six>=1.9.0'
    ],
    dependency_links=[],
    ext_modules=[],
    extras_require={
        'security': ['pyOpenSSL>=0.13', 'ndg-httpsclient', 'pyasn1'],
    },
)
