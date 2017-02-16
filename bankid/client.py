#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`bankid.client` -- BankID Client
=====================================

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2014-09-09, 16:55

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import warnings
import six
import base64
import datetime

import requests
from suds.client import Client
from suds.transport.http import HttpAuthenticated
from suds.transport import Reply
from suds import WebFault
from suds.sax.text import Text
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

    """

    def __init__(self, certificates, test_server=False):
        self.certs = certificates

        if test_server:
            self.api_url = 'https://appapi.test.bankid.com/rp/v4'
            self.wsdl_url = 'https://appapi.test.bankid.com/rp/v4?wsdl'
            self.verify_cert = resource_filename('bankid.certs', 'appapi.test.bankid.com.pem')
        else:
            self.api_url = 'https://appapi.bankid.com/rp/v4'
            self.wsdl_url = 'https://appapi.bankid.com/rp/v4?wsdl'
            self.verify_cert = resource_filename('bankid.certs', 'appapi.bankid.com.pem')

        headers = {
            "Content-Type": "text/xml;charset=UTF-8",
            "SOAPAction": ""
        }
        t = RequestsTransport(cert=self.certs, verify_cert=self.verify_cert)
        self.client = Client(self.wsdl_url, location=self.api_url,
                             headers=headers, transport=t)

    def authenticate(self, personal_number, **kwargs):
        """Request an authentication order. The :py:meth:`collect` method
        is used to query the status of the order.

        :param personal_number: The Swedish personal number in format YYYYMMDDXXXX.
        :type personal_number: str
        :return: The OrderResponse parsed to a dictionary.
        :rtype: dict
        :raises BankIDError: raises a subclass of this error
                             when error has been returned from server.

        """
        if 'requirementAlternatives' in kwargs:
            warnings.warn("Requirement Alternatives option is not tested.", BankIDWarning)

        try:
            out = self.client.service.Authenticate(
                personalNumber=personal_number, **kwargs)
        except WebFault as e:
            raise get_error_class(e, "Could not complete Authenticate order.")

        return self._dictify(out)

    def sign(self, user_visible_data, personal_number=None, **kwargs):
        """Request an signing order. The :py:meth:`collect` method
        is used to query the status of the order.

        :param user_visible_data: The information that the end user is requested to sign.
        :type user_visible_data: str
        :param personal_number: The Swedish personal number in format YYYYMMDDXXXX.
        :type personal_number: str
        :return: The OrderResponse parsed to a dictionary.
        :rtype: dict
        :raises BankIDError: raises a subclass of this error
                     when error has been returned from server.

        """
        if 'requirementAlternatives' in kwargs:
            warnings.warn("Requirement Alternatives option is not tested.", BankIDWarning)

        try:
            out = self.client.service.Sign(
                userVisibleData=six.text_type(base64.b64encode(six.b(user_visible_data)), encoding='utf-8'),
                personalNumber=personal_number, **kwargs)
        except WebFault as e:
            raise get_error_class(e, "Could not complete Sign order.")

        return self._dictify(out)

    def collect(self, order_ref):
        """Collect the progress status of the order with the specified
        order reference.

        :param order_ref: The UUID string specifying which order to collect status from.
        :type order_ref: str
        :return: The CollectResponse parsed to a dictionary.
        :rtype: dict
        :raises BankIDError: raises a subclass of this error
                             when error has been returned from server.

        """
        try:
            out = self.client.service.Collect(orderRef=order_ref)
        except WebFault as e:
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
        """Transforms the replies from :py:mod:`suds` own types to a
        regular Python dict with strings and datetimes.

        Tested with BankID version 2.5 return data.

        :param doc: The response as interpreted by :py:mod:`suds`.
        :returns: The response parsed to a dict.
        :rtype: dict

        """
        doc = dict(doc)
        out = {}
        try:
            for k in doc:
                k = _to_unicode(k)
                if isinstance(doc[k], Text):
                    out[k] = _to_unicode(doc[k])
                elif isinstance(doc[k], datetime.datetime):
                    out[k] = doc[k]
                else:
                    out[k] = self._dictify(doc[k])
        except:
            out = doc

        return out


def _to_unicode(s):
    if isinstance(s, Text):
        return six.text_type(s.unescape())
    elif isinstance(s, six.text_type):
        return s
    elif isinstance(s, six.binary_type):
        return s.decode('utf-8')


class RequestsTransport(HttpAuthenticated):
    """A Requests-based transport for suds, enabling the use of https and
    certificates when communicating with the SOAP service.

    Code has been adapted from this `Stack Overflow post
    <http://stackoverflow.com/questions/6277027/suds-over-https-with-cert>`_.

    """
    def __init__(self, **kwargs):
        self.requests_session = requests.Session()
        self.requests_session.cert = kwargs.pop('cert', None)
        self.requests_session.verify = kwargs.pop('verify_cert', None)
        # `super` won't work because HttpAuthenticated does not use new style class.
        HttpAuthenticated.__init__(self, **kwargs)

    def open(self, request):
        """Fetches the WSDL specification using certificates."""
        self.addcredentials(request)
        resp = self.requests_session.get(request.url,
                                         data=request.message,
                                         headers=request.headers)
        result = six.BytesIO(resp.content)
        return result

    def send(self, request):
        """Posts to SOAP service using certificates."""
        self.addcredentials(request)
        resp = self.requests_session.post(request.url,
                                          data=request.message,
                                          headers=request.headers)
        result = Reply(resp.status_code, resp.headers, resp.content)
        return result
