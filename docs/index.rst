.. PyBankID documentation master file, created by
   sphinx-quickstart on Fri Mar 18 07:23:13 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyBankID Documentation
======================

.. image:: https://travis-ci.org/hbldh/pybankid.svg?branch=master
    :target: https://travis-ci.org/hbldh/pybankid
.. image:: https://readthedocs.org/projects/pybankid/badge/?version=latest
    :target: http://pybankid.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: http://img.shields.io/pypi/v/pybankid.svg
    :target: https://pypi.python.org/pypi/pybankid/
.. image:: http://img.shields.io/pypi/dm/pybankid.svg
    :target: https://pypi.python.org/pypi/pybankid/
.. image:: http://img.shields.io/pypi/l/pybankid.svg
    :target: https://pypi.python.org/pypi/pybankid/
.. image:: https://coveralls.io/repos/github/hbldh/pybankid/badge.svg?branch=master
    :target: https://coveralls.io/github/hbldh/pybankid?branch=master

PyBankID is a client for performing BankID authentication and signing.

The Swedish BankID solution for digital signing uses a SOAP
connection solution, and this module aims at providing a simplifying
client for making authentication, signing and collect requests to
the BankID servers.

.. toctree::
   :maxdepth: 2

   usage
   client
   exceptions
   certutils


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

