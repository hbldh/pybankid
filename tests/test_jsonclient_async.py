import uuid

import pytest

import bankid


@pytest.mark.asyncio
async def test_authentication_and_collect(cert_and_key, ip_address, random_personal_number):
    """Authenticate call and then collect with the returned orderRef UUID."""
    c = bankid.AsyncBankIDJSONClient(certificates=cert_and_key, test_server=True)
    assert "appapi2.test.bankid.com.pem" in c.verify_cert
    out = await c.authenticate(ip_address, random_personal_number)
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    uuid.UUID(out.get("orderRef"), version=4)
    collect_status = await c.collect(out.get("orderRef"))
    assert collect_status.get("status") == "pending"
    assert collect_status.get("hintCode") in ("outstandingTransaction", "noClient")


@pytest.mark.asyncio
async def test_sign_and_collect(cert_and_key, ip_address, random_personal_number):
    """Sign call and then collect with the returned orderRef UUID."""

    c = bankid.AsyncBankIDJSONClient(certificates=cert_and_key, test_server=True)
    out = await c.sign(
        ip_address,
        "The data to be signed",
        personal_number=random_personal_number,
        user_non_visible_data="Non visible data",
    )
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    uuid.UUID(out.get("orderRef"), version=4)
    collect_status = await c.collect(out.get("orderRef"))
    assert collect_status.get("status") == "pending"
    assert collect_status.get("hintCode") in ("outstandingTransaction", "noClient")


@pytest.mark.asyncio
async def test_invalid_orderref_raises_error(cert_and_key):
    c = bankid.AsyncBankIDJSONClient(certificates=cert_and_key, test_server=True)
    with pytest.raises(bankid.exceptions.InvalidParametersError):
        await c.collect("invalid-uuid")


@pytest.mark.asyncio
async def test_already_in_progress_raises_error(cert_and_key, ip_address, random_personal_number):
    c = bankid.AsyncBankIDJSONClient(certificates=cert_and_key, test_server=True)
    await c.authenticate(ip_address, random_personal_number)
    with pytest.raises(bankid.exceptions.AlreadyInProgressError):
        await c.authenticate(ip_address, random_personal_number)


@pytest.mark.asyncio
async def test_already_in_progress_raises_error_2(cert_and_key, ip_address, random_personal_number):
    c = bankid.AsyncBankIDJSONClient(certificates=cert_and_key, test_server=True)
    await c.sign(ip_address, "Text to sign", random_personal_number)
    with pytest.raises(bankid.exceptions.AlreadyInProgressError):
        await c.sign(ip_address, "Text to sign", random_personal_number)


@pytest.mark.asyncio
async def test_authentication_and_cancel(cert_and_key, ip_address, random_personal_number):
    """Authenticate call and then cancel it"""
    c = bankid.AsyncBankIDJSONClient(certificates=cert_and_key, test_server=True)
    out = await c.authenticate(ip_address, random_personal_number)
    assert isinstance(out, dict)
    # UUID.__init__ performs the UUID compliance assertion.
    order_ref = uuid.UUID(out.get("orderRef"), version=4)
    collect_status = await c.collect(out.get("orderRef"))
    assert collect_status.get("status") == "pending"
    assert collect_status.get("hintCode") in ("outstandingTransaction", "noClient")
    success = await c.cancel(str(order_ref))
    assert success
    with pytest.raises(bankid.exceptions.InvalidParametersError):
        collect_status = await c.collect(out.get("orderRef"))


@pytest.mark.asyncio
async def test_cancel_with_invalid_uuid(cert_and_key):
    c = bankid.AsyncBankIDJSONClient(certificates=cert_and_key, test_server=True)
    invalid_order_ref = uuid.uuid4()
    with pytest.raises(bankid.exceptions.InvalidParametersError):
        await c.cancel(str(invalid_order_ref))
