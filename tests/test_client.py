#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`test_client`
==================

.. module:: test_client
   :platform: Unix, Windows
   :synopsis:

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2015-08-07, 12:00

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import random
import uuid

import pytest
try:
    from unittest import mock
except:
    import mock

import bankid


def _get_random_personal_number():
    """Simple random Swedish personal number generator."""

    def _luhn_digit(id_):
        """Calculate Luhn control digit for personal number.

        Code adapted from `Faker <https://github.com/joke2k/faker/blob/master/faker/providers/ssn/sv_SE/__init__.py>`_.

        :param id_: The partial number to calculate checksum of.
        :type id_: str
        :return: Integer digit in [0, 9].
        :rtype: int

        """

        def digits_of(n):
            return [int(i) for i in str(n)]
        id_ = int(id_) * 10
        digits = digits_of(id_)
        checksum = sum(digits[-1::-2])
        for k in digits[-2::-2]:
            checksum += sum(digits_of(k * 2))
        checksum %= 10

        return checksum if checksum == 0 else 10 - checksum

    year = random.randint(1900, 2014)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    suffix = random.randint(0, 999)
    pn = "{0:04d}{1:02d}{2:02d}{3:03d}".format(year, month, day, suffix)
    return pn + str(_luhn_digit(pn[2:]))


def test_authentication_and_collect_1(cert_and_key):
    """Authenticate call and then collect with the returned orderRef UUID."""

    c = bankid.BankIDClient(certificates=cert_and_key, test_server=True, legacy_mode=True)
    assert 'appapi.test.bankid.com.pem' in c.verify_cert
    out = c.authenticate(_get_random_personal_number())
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    order_ref = uuid.UUID(out.get('orderRef'), version=4)
    collect_status = c.collect(out.get('orderRef'))
    assert collect_status.get('progressStatus') in ('OUTSTANDING_TRANSACTION', 'NO_CLIENT')


def test_authentication_and_collect_2(cert_and_key):
    """Authenticate call and then collect with the returned orderRef UUID."""

    c = bankid.BankIDClient(certificates=cert_and_key, test_server=True)
    assert 'appapi2.test.bankid.com.pem' in c.verify_cert
    out = c.authenticate(_get_random_personal_number())
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    order_ref = uuid.UUID(out.get('orderRef'), version=4)
    collect_status = c.collect(out.get('orderRef'))
    assert collect_status.get('progressStatus') in ('OUTSTANDING_TRANSACTION', 'NO_CLIENT')


def test_sign_and_collect(cert_and_key):
    """Sign call and then collect with the returned orderRef UUID."""

    c = bankid.BankIDClient(certificates=cert_and_key, test_server=True)
    out = c.sign("The data to be signed", _get_random_personal_number())
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    order_ref = uuid.UUID(out.get('orderRef'), version=4)
    collect_status = c.collect(out.get('orderRef'))
    assert collect_status.get('progressStatus') in ('OUTSTANDING_TRANSACTION', 'NO_CLIENT')


def test_invalid_orderref_raises_error(cert_and_key):
    c = bankid.BankIDClient(certificates=cert_and_key, test_server=True)
    with pytest.raises(bankid.exceptions.InvalidParametersError):
        collect_status = c.collect('invalid-uuid')


def test_already_in_progress_raises_error(cert_and_key):
    c = bankid.client.BankIDClient(certificates=cert_and_key, test_server=True)
    pn = _get_random_personal_number()
    out = c.authenticate(pn)
    with pytest.raises(bankid.exceptions.AlreadyInProgressError):
        out2 = c.authenticate(pn)


def test_already_in_progress_raises_error_2(cert_and_key):
    c = bankid.client.BankIDClient(certificates=cert_and_key, test_server=True)
    pn = _get_random_personal_number()
    out = c.sign('Text to sign', pn)
    with pytest.raises(bankid.exceptions.AlreadyInProgressError):
        out2 = c.sign('Text to sign', pn)


def test_file_sign_not_implemented(cert_and_key):
    c = bankid.client.BankIDClient(certificates=cert_and_key, test_server=True)
    with pytest.raises(NotImplementedError):
        out = c.file_sign()


@pytest.mark.parametrize("legacy_mode,endpoint", [
    (False, 'appapi2.bankid.com'),
    (True, 'appapi.bankid.com'),
])
def test_correct_prod_server_urls(cert_and_key, legacy_mode, endpoint):
    bankid.client.Client.__init__ = mock.MagicMock(return_value=None)
    c = bankid.client.BankIDClient(
        certificates=cert_and_key,
        test_server=False,
        legacy_mode=legacy_mode)
    assert c.api_url == 'https://{0}/rp/v4'.format(endpoint)
    assert c.wsdl_url == 'https://{0}/rp/v4?wsdl'.format(endpoint)
    assert '{0}.pem'.format(endpoint) in c.verify_cert


@pytest.mark.parametrize("legacy_mode,endpoint", [
    (False, 'appapi2.bankid.com'),
    (True, 'appapi.bankid.com'),
])
def test_correct_prod_server_urls_2(cert_and_key, legacy_mode, endpoint):
    bankid.client.Client.__init__ = mock.MagicMock(return_value=None)
    c = bankid.client.BankIDClient(
        certificates=cert_and_key,
        legacy_mode=legacy_mode)
    assert c.api_url == 'https://{0}/rp/v4'.format(endpoint)
    assert c.wsdl_url == 'https://{0}/rp/v4?wsdl'.format(endpoint)
    assert '{0}.pem'.format(endpoint) in c.verify_cert
