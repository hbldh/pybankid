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

import re
from codecs import open
from setuptools import setup, find_packages


with open('bankid/version.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)


def read(f):
    return open(f, encoding='utf-8').read()


setup(
    name='pybankid',
    version=version,
    author='Henrik Blidh',
    author_email='henrik.blidh@nedomkull.com',
    description="BankID client for Python",
    long_description=read('README.rst'),
    license='MIT',
    url='https://github.com/hbldh/pybankid/',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Security',
        'Topic :: Utilities',
    ],
    platforms=['Linux', 'Mac OSX', 'Windows XP/Vista/7/8'],
    packages=find_packages(exclude=('tests', )),
    package_data={'': ['*.pem']},
    install_requires=read('requirements.txt').strip().splitlines(),
    dependency_links=[],
    ext_modules=[],
    extras_require={
        'security': ['pyOpenSSL>=0.13', 'ndg-httpsclient', 'pyasn1'],
    },
)
