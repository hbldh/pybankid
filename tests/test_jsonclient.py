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
import tempfile
import uuid

import pytest

try:
    from unittest import mock
except:
    import mock
import requests

import bankid


def _get_random_personal_number():
    """Simple random Swedish personal number generator."""

    def _luhn_digit(id_):
        """Calculate Luhn control digit for personal number.

        Code adapted from `Faker
        <https://github.com/joke2k/faker/blob/master/faker/providers/ssn
        /sv_SE/__init__.py>`_.

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


def test_authentication_and_collect(cert_and_key, ip_address):
    """Authenticate call and then collect with the returned orderRef UUID."""

    c = bankid.BankIDJSONClient(certificates=cert_and_key, test_server=True)
    assert 'appapi2.test.bankid.com.pem' in c.verify_cert
    out = c.authenticate(ip_address, _get_random_personal_number())
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    order_ref = uuid.UUID(out.get('orderRef'), version=4)
    collect_status = c.collect(out.get('orderRef'))
    assert collect_status.get('status') == 'pending'
    assert collect_status.get('hintCode') in \
           ('outstandingTransaction', 'noClient')


def test_sign_and_collect(cert_and_key, ip_address):
    """Sign call and then collect with the returned orderRef UUID."""

    c = bankid.BankIDJSONClient(certificates=cert_and_key, test_server=True)
    out = c.sign(ip_address, "The data to be signed",
                 personal_number=_get_random_personal_number(),
                 user_non_visible_data="Non visible data")
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    order_ref = uuid.UUID(out.get('orderRef'), version=4)
    collect_status = c.collect(out.get('orderRef'))
    assert collect_status.get('status') == 'pending'
    assert collect_status.get('hintCode') in \
           ('outstandingTransaction', 'noClient')


def test_invalid_orderref_raises_error(cert_and_key):
    c = bankid.BankIDJSONClient(certificates=cert_and_key, test_server=True)
    with pytest.raises(bankid.exceptions.InvalidParametersError):
        collect_status = c.collect('invalid-uuid')


def test_already_in_progress_raises_error(cert_and_key, ip_address):
    c = bankid.BankIDJSONClient(certificates=cert_and_key, test_server=True)
    pn = _get_random_personal_number()
    out = c.authenticate(ip_address, pn)
    with pytest.raises(bankid.exceptions.AlreadyInProgressError):
        out2 = c.authenticate(ip_address, pn)


def test_already_in_progress_raises_error_2(cert_and_key, ip_address):
    c = bankid.BankIDJSONClient(certificates=cert_and_key, test_server=True)
    pn = _get_random_personal_number()
    out = c.sign(ip_address, 'Text to sign', pn)
    with pytest.raises(bankid.exceptions.AlreadyInProgressError):
        out2 = c.sign(ip_address, 'Text to sign', pn)


def test_authentication_and_cancel(cert_and_key, ip_address):
    """Authenticate call and then cancel it"""

    c = bankid.BankIDJSONClient(certificates=cert_and_key, test_server=True)
    out = c.authenticate(ip_address, _get_random_personal_number())
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    order_ref = uuid.UUID(out.get('orderRef'), version=4)
    collect_status = c.collect(out.get('orderRef'))
    assert collect_status.get('status') == 'pending'
    assert collect_status.get('hintCode') in \
           ('outstandingTransaction', 'noClient')
    success = c.cancel(str(order_ref))
    assert success
    with pytest.raises(bankid.exceptions.InvalidParametersError):
        collect_status = c.collect(out.get('orderRef'))


def test_cancel_with_invalid_uuid(cert_and_key):
    c = bankid.BankIDJSONClient(certificates=cert_and_key, test_server=True)
    invalid_order_ref = uuid.uuid4()
    with pytest.raises(bankid.exceptions.InvalidParametersError):
        cancel_status = c.cancel(str(invalid_order_ref))


@pytest.mark.parametrize("test_server, endpoint", [
    (False, 'appapi2.bankid.com'),
    (True, 'appapi2.test.bankid.com'),
])
def test_correct_prod_server_urls(cert_and_key, test_server, endpoint):
    c = bankid.BankIDJSONClient(
        certificates=cert_and_key,
        test_server=test_server)
    assert c.api_url == 'https://{0}/rp/v5/'.format(endpoint)
    assert '{0}.pem'.format(endpoint) in c.verify_cert
