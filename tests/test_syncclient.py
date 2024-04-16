#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`test_syncclient`
======================

.. module:: test_syncclient
   :platform: Unix, Windows
   :synopsis:

.. moduleauthor:: mxamin <amin.solhizadeh@gmail.com>

Created on 2024-01-18

"""
import uuid

import pytest
from typing import Tuple

try:
    from unittest import mock
except:
    import mock  # type: ignore[no-redef]

from bankid import BankIDClient, exceptions


def test_authentication_and_collect(cert_and_key: Tuple[str, str], ip_address: str, random_personal_number: str) -> None:
    """Authenticate call and then collect with the returned orderRef UUID."""

    c = BankIDClient(certificates=cert_and_key, test_server=True)
    assert "appapi2.test.bankid.com.pem" in str(c.verify_cert)
    out = c.authenticate(ip_address, requirement={"personalNumber": random_personal_number})
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    order_ref = uuid.UUID(out["orderRef"], version=4)
    collect_status = c.collect(str(order_ref))
    assert collect_status["status"] == "pending"
    assert collect_status["hintCode"] in ("outstandingTransaction", "noClient")


def test_sign_and_collect(cert_and_key: Tuple[str, str], ip_address: str) -> None:
    """Sign call and then collect with the returned orderRef UUID."""

    c = BankIDClient(certificates=cert_and_key, test_server=True)
    out = c.sign(
        ip_address,
        user_visible_data="The data to be signed",
        user_non_visible_data="Non visible data",
    )
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    order_ref = uuid.UUID(out["orderRef"], version=4)
    collect_status = c.collect(str(order_ref))
    assert collect_status["status"] == "pending"
    assert collect_status["hintCode"] in ("outstandingTransaction", "noClient")


def test_phone_sign_and_collect(cert_and_key: Tuple[str, str], random_personal_number: str) -> None:
    """Phone sign call and then collect with the returned orderRef UUID."""

    c = BankIDClient(certificates=cert_and_key, test_server=True)
    out = c.phone_sign(random_personal_number, "user", user_visible_data="The data to be signed")
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    order_ref = uuid.UUID(out["orderRef"], version=4)
    collect_status = c.collect(str(order_ref))
    assert collect_status["status"] == "pending"
    assert collect_status["hintCode"] in ("outstandingTransaction", "noClient")


def test_invalid_orderref_raises_error(cert_and_key: Tuple[str, str]) -> None:
    c = BankIDClient(certificates=cert_and_key, test_server=True)
    with pytest.raises(exceptions.InvalidParametersError):
        collect_status = c.collect("invalid-uuid")


def test_already_in_progress_raises_error(cert_and_key: Tuple[str, str], ip_address: str, random_personal_number: str) -> None:
    c = BankIDClient(certificates=cert_and_key, test_server=True)
    out = c.authenticate(ip_address, requirement={"personalNumber": random_personal_number})
    with pytest.raises(exceptions.AlreadyInProgressError):
        out2 = c.authenticate(ip_address, requirement={"personalNumber": random_personal_number})


def test_already_in_progress_raises_error_2(cert_and_key: Tuple[str, str], ip_address: str, random_personal_number: str) -> None:
    c = BankIDClient(certificates=cert_and_key, test_server=True)
    out = c.sign(ip_address, requirement={"personalNumber": random_personal_number}, user_visible_data="Text to sign")
    with pytest.raises(exceptions.AlreadyInProgressError):
        out2 = c.sign(
            ip_address, requirement={"personalNumber": random_personal_number}, user_visible_data="Text to sign"
        )


def test_authentication_and_cancel(cert_and_key: Tuple[str, str], ip_address: str, random_personal_number: str) -> None:
    """Authenticate call and then cancel it"""

    c = BankIDClient(certificates=cert_and_key, test_server=True)
    out = c.authenticate(ip_address, requirement={"personalNumber": random_personal_number})
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    order_ref = uuid.UUID(out["orderRef"], version=4)
    collect_status = c.collect(str(order_ref))
    assert collect_status["status"] == "pending"
    assert collect_status["hintCode"] in ("outstandingTransaction", "noClient")
    success = c.cancel(str(order_ref))
    assert success
    with pytest.raises(exceptions.InvalidParametersError):
        collect_status = c.collect(str(order_ref))


def test_phone_authentication_and_cancel(cert_and_key: Tuple[str, str], random_personal_number: str) -> None:
    """Phone authenticate call and then cancel it"""

    c = BankIDClient(certificates=cert_and_key, test_server=True)
    out = c.phone_authenticate(random_personal_number, "user")
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    order_ref = uuid.UUID(out["orderRef"], version=4)
    collect_status = c.collect(str(order_ref))
    assert collect_status["status"] == "pending"
    assert collect_status["hintCode"] in ("outstandingTransaction", "noClient")
    success = c.cancel(str(order_ref))
    assert success
    with pytest.raises(exceptions.InvalidParametersError):
        collect_status = c.collect(str(order_ref))


def test_cancel_with_invalid_uuid(cert_and_key: Tuple[str, str]) -> None:
    c = BankIDClient(certificates=cert_and_key, test_server=True)
    invalid_order_ref = uuid.uuid4()
    with pytest.raises(exceptions.InvalidParametersError):
        cancel_status = c.cancel(str(invalid_order_ref))


@pytest.mark.parametrize(
    "test_server, endpoint",
    [(False, "appapi2.bankid.com"), (True, "appapi2.test.bankid.com")],
)
def test_correct_prod_server_urls(cert_and_key: Tuple[str, str], test_server: bool, endpoint: str) -> None:
    c = BankIDClient(certificates=cert_and_key, test_server=test_server)
    assert c.api_url == "https://{0}/rp/v6.0/".format(endpoint)
    assert "{0}.pem".format(endpoint) in str(c.verify_cert)
