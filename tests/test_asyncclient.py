"""
:mod:`test_asyncclient`
=======================

.. module:: test_asyncclient
   :platform: Unix, Windows
   :synopsis:

.. moduleauthor:: tiwilliam <william@defunct.cc>

Created on 2023-12-15

"""

import uuid

import pytest
from typing import Tuple

from bankid import BankIDAsyncClient, exceptions


@pytest.mark.asyncio
async def test_authentication_and_collect(cert_and_key: Tuple[str, str], ip_address: str) -> None:
    """Authenticate call and then collect with the returned orderRef UUID."""
    c = BankIDAsyncClient(certificates=cert_and_key, test_server=True)
    assert "appapi2.test.bankid.com.pem" in str(c.verify_cert)
    out = await c.authenticate(ip_address)

    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    order_ref = uuid.UUID(out["orderRef"], version=4)
    collect_status = await c.collect(str(order_ref))
    assert collect_status.get("status") == "pending"
    assert collect_status.get("hintCode") in ("outstandingTransaction", "noClient")


@pytest.mark.asyncio
async def test_sign_and_collect(cert_and_key: Tuple[str, str], ip_address: str) -> None:
    """Sign call and then collect with the returned orderRef UUID."""

    c = BankIDAsyncClient(certificates=cert_and_key, test_server=True)
    out = await c.sign(
        ip_address,
        user_visible_data="The data to be signed",
        user_non_visible_data="Non visible data",
    )
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    order_ref = uuid.UUID(out["orderRef"], version=4)
    collect_status = await c.collect(str(order_ref))
    assert collect_status.get("status") == "pending"
    assert collect_status.get("hintCode") in ("outstandingTransaction", "noClient")


@pytest.mark.asyncio
async def test_phone_sign_and_collect(cert_and_key: Tuple[str, str], random_personal_number: str) -> None:
    """Phone sign call and then collect with the returned orderRef UUID."""

    c = BankIDAsyncClient(certificates=cert_and_key, test_server=True)
    out = await c.phone_sign(random_personal_number, "RP", user_visible_data="The data to be signed")
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    order_ref = uuid.UUID(out["orderRef"], version=4)
    collect_status = await c.collect(str(order_ref))
    assert collect_status.get("status") == "pending"
    assert collect_status.get("hintCode") in ("outstandingTransaction", "noClient")


@pytest.mark.asyncio
async def test_invalid_orderref_raises_error(cert_and_key: Tuple[str, str]) -> None:
    c = BankIDAsyncClient(certificates=cert_and_key, test_server=True)
    with pytest.raises(exceptions.InvalidParametersError):
        await c.collect("invalid-uuid")


@pytest.mark.asyncio
async def test_already_in_progress_raises_error(cert_and_key: Tuple[str, str], ip_address: str, random_personal_number: str) -> None:
    c = BankIDAsyncClient(certificates=cert_and_key, test_server=True)
    await c.authenticate(ip_address, requirement={"personalNumber": random_personal_number})
    with pytest.raises(exceptions.AlreadyInProgressError):
        await c.authenticate(ip_address, requirement={"personalNumber": random_personal_number})


@pytest.mark.asyncio
async def test_already_in_progress_raises_error_2(cert_and_key: Tuple[str, str], ip_address: str, random_personal_number: str) -> None:
    c = BankIDAsyncClient(certificates=cert_and_key, test_server=True)
    await c.sign(
        ip_address,
        requirement={"personalNumber": random_personal_number},
        user_visible_data="Text to sign",
    )
    with pytest.raises(exceptions.AlreadyInProgressError):
        await c.sign(
            ip_address, requirement={"personalNumber": random_personal_number}, user_visible_data="Text to sign"
        )


@pytest.mark.asyncio
async def test_authentication_and_cancel(cert_and_key: Tuple[str, str], ip_address: str) -> None:
    """Authenticate call and then cancel it"""
    c = BankIDAsyncClient(certificates=cert_and_key, test_server=True)
    out = await c.authenticate(ip_address)
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    order_ref = uuid.UUID(out["orderRef"], version=4)
    collect_status = await c.collect(str(order_ref))
    assert collect_status.get("status") == "pending"
    assert collect_status.get("hintCode") in ("outstandingTransaction", "noClient")
    success = await c.cancel(str(order_ref))
    assert success
    with pytest.raises(exceptions.InvalidParametersError):
        collect_status = await c.collect(str(order_ref))


@pytest.mark.asyncio
async def test_phone_authentication_and_cancel(cert_and_key: Tuple[str, str], random_personal_number: str) -> None:
    """Phone authenticate call and then cancel it"""

    c = BankIDAsyncClient(certificates=cert_and_key, test_server=True)
    out = await c.phone_authenticate(random_personal_number, "user")
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    order_ref = uuid.UUID(out["orderRef"], version=4)
    collect_status = await c.collect(str(order_ref))
    assert collect_status.get("status") == "pending"
    assert collect_status.get("hintCode") in ("outstandingTransaction", "noClient")
    success = await c.cancel(str(order_ref))
    assert success
    with pytest.raises(exceptions.InvalidParametersError):
        collect_status = await c.collect(str(order_ref))


@pytest.mark.asyncio
async def test_cancel_with_invalid_uuid(cert_and_key: Tuple[str, str]) -> None:
    c = BankIDAsyncClient(certificates=cert_and_key, test_server=True)
    invalid_order_ref = uuid.uuid4()
    with pytest.raises(exceptions.InvalidParametersError):
        await c.cancel(str(invalid_order_ref))
