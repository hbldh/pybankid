import random
from typing import Awaitable

import httpx
import pytest
import pytest_asyncio

from bankid.certs import get_test_cert_and_key


@pytest.fixture()
def ip_address() -> str:
    with httpx.Client() as client:
        response = client.get("https://httpbin.org/ip")
        return response.json()["origin"].split(",")[0]


@pytest_asyncio.fixture()
async def ip_address_async() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/ip")
        return response.json()["origin"].split(",")[0]


@pytest.fixture()
def cert_and_key():
    cert, key = get_test_cert_and_key()
    return str(cert), str(key)


@pytest.fixture()
def random_personal_number():
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
