# -*- coding: utf-8 -*-
"""
:mod:`setup`
============

.. module:: setup
   :platform: Unix, Windows
   :synopsis: Setup file for pybankid.

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2013-09-14, 19:31

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import bankid
from setuptools import setup, find_packages

setup(
    name='pybankid',
    version=bankid.__version__,
    description="BankID client for Python",
    author='Henrik Blidh',
    author_email='henrik.blidh@nedomkull.com',
    license='MIT',
    url='https://github.com/hbldh/pybankid',
    packages=find_packages(),
    package_data={'': ['*.pem']},
    install_requires=[
        'requests>=2.2.1',
        'suds>=0.4',
    ],
    dependency_links=[],
    ext_modules=[],
    entry_points={
    }
)
