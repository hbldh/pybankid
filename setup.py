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
    author=bankid.author,
    author_email=bankid.author_email,
    description=bankid.description,
    long_description=bankid.long_description,
    license=bankid.license,
    url=bankid.url,
    classifiers=bankid.classifiers,
    platforms=bankid.platforms,
    packages=find_packages(),
    package_data={'': ['*.pem']},
    install_requires=[line.strip() for line in open("requirements.txt")],
    dependency_links=[],
    ext_modules=[],
    entry_points={
    }
)
