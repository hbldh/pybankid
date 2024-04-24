import random

import pytest
from typing import List, Tuple

from bankid.certs import get_test_cert_and_key


@pytest.fixture(scope="session")
def ip_address() -> str:
    return "127.0.0.1"


@pytest.fixture()
def cert_and_key() -> Tuple[str, str]:
    cert, key = get_test_cert_and_key()
    return str(cert), str(key)


@pytest.fixture()
def random_personal_number() -> str:
    """Simple random Swedish personal number generator."""

    def _luhn_digit(id_: str) -> int:
        """Calculate Luhn control digit for personal number.

        Code adapted from `Faker
        <https://github.com/joke2k/faker/blob/master/faker/providers/ssn
        /sv_SE/__init__.py>`_.

        :param id_: The partial number to calculate checksum of.
        :type id_: str
        :return: Integer digit in [0, 9].
        :rtype: int

        """

        def digits_of(n: int) -> List[int]:
            return [int(i) for i in str(n)]

        digits = digits_of(int(id_) * 10)
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
