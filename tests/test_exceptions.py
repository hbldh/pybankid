from collections import namedtuple
import sys
from typing import Union

import pytest

import bankid

if sys.version_info >= (3, 9):
    from builtins import type as Type
else:
    # Remove once PyBankID no longer support Python 3.8 or lower
    from typing import Type


@pytest.mark.parametrize(
    "exception_class,rfa",
    [
        (bankid.exceptions.AlreadyInProgressError, 4),
        (bankid.exceptions.InvalidParametersError, None),
        (bankid.exceptions.UnauthorizedError, None),
        (bankid.exceptions.NotFoundError, None),
        (bankid.exceptions.RequestTimeoutError, 5),
        (bankid.exceptions.InternalError, 5),
        (bankid.exceptions.MaintenanceError, 5),
        (bankid.exceptions.BankIDError, None),
    ],
)
def test_exceptions(exception_class: Type[Exception], rfa: Union[int, None]) -> None:
    e = exception_class()
    assert isinstance(e, bankid.exceptions.BankIDError)
    assert e.rfa == rfa


@pytest.mark.parametrize(
    "exception_class,error_code",
    [
        (bankid.exceptions.AlreadyInProgressError, "alreadyInProgress"),
        (bankid.exceptions.InvalidParametersError, "invalidParameters"),
        (bankid.exceptions.UnauthorizedError, "unauthorized"),
        (bankid.exceptions.NotFoundError, "notFound"),
        (bankid.exceptions.RequestTimeoutError, "requestTimeout"),
        (bankid.exceptions.InternalError, "internalError"),
        (bankid.exceptions.MaintenanceError, "maintenance"),
        (bankid.exceptions.BankIDError, "Unknown error code"),
    ],
)
def test_error_class_factory(exception_class: Type[Exception], error_code: str) -> None:
    MockResponse = namedtuple("MockResponse", ["json"])
    response = MockResponse(json=lambda: {"errorCode": error_code})
    # error: Argument 1 to "get_json_error_class" has incompatible type "MockResponse@41"; expected "Response"  [arg-type]
    e_class = bankid.exceptions.get_json_error_class(response)  # type: ignore[arg-type]
    assert isinstance(e_class, exception_class)
