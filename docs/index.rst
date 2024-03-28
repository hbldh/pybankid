.. PyBankID documentation master file, created by
   sphinx-quickstart on Fri Mar 18 07:23:13 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyBankID Documentation
======================

.. image:: https://github.com/hbldh/pybankid/workflows/Build%20and%20Test/badge.svg
    :target: https://github.com/hbldh/pybankid/actions?query=workflow%3A%22Build+and+Test%22
.. image:: https://readthedocs.org/projects/pybankid/badge/?version=latest
    :target: http://pybankid.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: http://img.shields.io/pypi/v/pybankid.svg
    :target: https://pypi.python.org/pypi/pybankid/
.. image:: http://img.shields.io/pypi/l/pybankid.svg
    :target: https://pypi.python.org/pypi/pybankid/
.. image:: https://coveralls.io/repos/github/hbldh/pybankid/badge.svg?branch=master
    :target: https://coveralls.io/github/hbldh/pybankid?branch=master

PyBankID is a client for providing BankID services as a Relying Party, i.e.
providing authentication and signing functionality to end users. This package
provides a simplifying interface for initiating authentication
and signing orders and then collecting the results from the BankID servers.

The only supported BankID API version supported by PyBankID from version 1.0.0
is v6.0, which means that the Secure Start solution is the only supported way
of providing BankID services. PyBankID versions prior to 1.0.0 will not
work after 1st of May 2024.

If you intend to use PyBankID in your project, you are advised to read
the `BankID Integration Guide
<https://www.bankid.com/en/utvecklare/guider/teknisk-integrationsguide>`_ before
doing anything else. There, one can find information
about how the BankID methods are defined and how to use them.


.. toctree::
   :maxdepth: 2

   get_started
   certutils
   examples
   api_reference


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

