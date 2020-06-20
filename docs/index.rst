.. PyBankID documentation master file, created by
   sphinx-quickstart on Fri Mar 18 07:23:13 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyBankID Documentation
======================

.. image:: https://dev.azure.com/hbldh/github/_apis/build/status/hbldh.pybankid?branchName=master
    :target: https://dev.azure.com/hbldh/github/_build/latest?definitionId=2&branchName=master
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

If you intend to use PyBankID in your project, you are advised to read
the `BankID Relying Party Guidelines
<https://www.bankid.com/utvecklare/rp-info>`_ before
doing anything else. There, one can find information
about how the BankID methods are defined and how to use them.

**If you use PyBankID in production and want updates on new releases and
notifications about important changes to the BankID service, send a mail to
the developer of this package to be added to the PyBankID mailing list.**


.. toctree::
   :maxdepth: 2

   get_started
   usage
   exceptions
   certutils


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

