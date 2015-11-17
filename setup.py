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
    author=bankid._author,
    author_email=bankid._author_email,
    description=bankid._description,
    long_description=bankid._long_description,
    license=bankid.__license__,
    url=bankid._url,
    classifiers=bankid._classifiers,
    platforms=bankid._platforms,
    packages=find_packages(exclude=('tests', )),
    package_data={'': ['*.pem']},
    install_requires=[
        'requests>=2.7.0',
        'suds-jurko>=0.6',
        'six>=1.9.0'
    ],
    dependency_links=[],
    ext_modules=[],
    entry_points={
    }
)
