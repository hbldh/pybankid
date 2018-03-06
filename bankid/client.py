#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`bankid.client` -- BankID Client
=====================================

Created on 2014-09-09 by hbldh

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import warnings
import six
import base64

import requests
from zeep import Client
from zeep.transports import Transport
from zeep.exceptions import Error
from pkg_resources import resource_filename

from bankid.exceptions import get_error_class, BankIDWarning

# Handling Python 2.7 verification of certificates with urllib3.
# See README.rst for details.
try:
    import requests.packages.urllib3.contrib.pyopenssl
    requests.packages.urllib3.contrib.pyopenssl.inject_into_urllib3()
except ImportError:
    if bool(os.environ.get('PYBANKID_DISABLE_WARNINGS', False)):
        requests.packages.urllib3.disable_warnings()


class BankIDClient(object):
    """The client to use for communicating with BankID servers.

    :param certificates: Tuple of string paths to the certificate to use and
        the key to sign with.
    :type certificates: tuple
    :param test_server: Use the test server for authenticating and signing.
    :type test_server: bool
    :param legacy_mode: Use the old production server endpoint (will be removed
        in June 2019)
    :type legacy_mode: bool

    """

    def __init__(self, certificates, test_server=False, legacy_mode=False):
        self.certs = certificates

        if legacy_mode:
            warnings.warn("BankIDClient using the SOAP API in legacy mode will "
                          "be deprecated in March 2019. Use "
                          "bankid.BankIDJSONClient instead.",
                          PendingDeprecationWarning)
        else:
            warnings.warn("BankIDClient using the SOAP API will "
                          "be deprecated in February 2020. Use "
                          "bankid.BankIDJSONClient instead.",
                          PendingDeprecationWarning)

        if test_server:
            if legacy_mode:
                self.api_url = 'https://appapi.test.bankid.com/rp/v4'
                self.wsdl_url = 'https://appapi.test.bankid.com/rp/v4?wsdl'
                self.verify_cert = resource_filename(
                    'bankid.certs', 'appapi.test.bankid.com.pem')
            else:
                self.api_url = 'https://appapi2.test.bankid.com/rp/v4'
                self.wsdl_url = 'https://appapi2.test.bankid.com/rp/v4?wsdl'
                self.verify_cert = resource_filename(
                    'bankid.certs', 'appapi2.test.bankid.com.pem')
        else:
            if legacy_mode:
                # Use the old appapi.bankid.com endpoint.
                self.api_url = 'https://appapi.bankid.com/rp/v4'
                self.wsdl_url = 'https://appapi.bankid.com/rp/v4?wsdl'
                self.verify_cert = resource_filename(
                    'bankid.certs', 'appapi.bankid.com.pem')

            else:
                self.api_url = 'https://appapi2.bankid.com/rp/v4'
                self.wsdl_url = 'https://appapi2.bankid.com/rp/v4?wsdl'
                self.verify_cert = resource_filename(
                    'bankid.certs', 'appapi2.bankid.com.pem')

        headers = {
            "Content-Type": "text/xml;charset=UTF-8",
        }

        session = requests.Session()
        session.verify = self.verify_cert
        session.cert = self.certs
        session.headers = headers
        transport = Transport(session=session)
        self.client = Client(self.wsdl_url, transport=transport)

    def authenticate(self, personal_number, **kwargs):
        """Request an authentication order. The :py:meth:`collect` method
        is used to query the status of the order.

        :param personal_number: The Swedish personal number
            in format YYYYMMDDXXXX.
        :type personal_number: str
        :return: The OrderResponse parsed to a dictionary.
        :rtype: dict
        :raises BankIDError: raises a subclass of this error
                             when error has been returned from server.

        """
        if 'requirementAlternatives' in kwargs:
            warnings.warn("Requirement Alternatives "
                          "option is not tested.", BankIDWarning)

        try:
            out = self.client.service.Authenticate(
                personalNumber=personal_number, **kwargs)
        except Error as e:
            raise get_error_class(e, "Could not complete Authenticate order.")

        return self._dictify(out)

    def sign(self, user_visible_data, personal_number=None, **kwargs):
        """Request an signing order. The :py:meth:`collect` method
        is used to query the status of the order.

        :param user_visible_data: The information that the end user is
            requested to sign.
        :type user_visible_data: str
        :param personal_number: The Swedish personal number in
            format YYYYMMDDXXXX.
        :type personal_number: str
        :return: The OrderResponse parsed to a dictionary.
        :rtype: dict
        :raises BankIDError: raises a subclass of this error
                     when error has been returned from server.

        """
        if 'requirementAlternatives' in kwargs:
            warnings.warn("Requirement Alternatives option is not tested.",
                          BankIDWarning)

        if isinstance(user_visible_data, six.text_type):
            data = base64.b64encode(
                user_visible_data.encode('utf-8')).decode('ascii')
        else:
            data = base64.b64encode(user_visible_data).decode('ascii')

        try:
            out = self.client.service.Sign(
                userVisibleData=data,
                personalNumber=personal_number, **kwargs)
        except Error as e:
            raise get_error_class(e, "Could not complete Sign order.")

        return self._dictify(out)

    def collect(self, order_ref):
        """Collect the progress status of the order with the specified
        order reference.

        :param order_ref: The UUID string specifying which order to
            collect status from.
        :type order_ref: str
        :return: The CollectResponse parsed to a dictionary.
        :rtype: dict
        :raises BankIDError: raises a subclass of this error
                             when error has been returned from server.

        """
        try:
            out = self.client.service.Collect(order_ref)
        except Error as e:
            raise get_error_class(e, "Could not complete Collect call.")

        return self._dictify(out)

    def file_sign(self, **kwargs):
        """Request a file signing order. The :py:meth:`collect` method
        is used to query the status of the order.

        .. note::

            Not implemented due to that the method is deprecated.

        :raises NotImplementedError: This method is not implemented.

        """
        raise NotImplementedError(
            "FileSign is deprecated and therefore not implemented.")

    def _dictify(self, doc):
        """Transforms the replies to a regular Python dict with
        strings and datetimes.

        Tested with BankID version 2.5 return data.

        :param doc: The response as interpreted by :py:mod:`zeep`.
        :returns: The response parsed to a dict.
        :rtype: dict

        """
        return {k: (self._dictify(doc[k]) if hasattr(doc[k], '_xsd_type')
                    else doc[k]) for k in doc}
