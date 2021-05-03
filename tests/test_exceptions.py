#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

import bankid


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
def test_exceptions(exception_class, rfa):
    e = exception_class()
    assert e.rfa == rfa
    assert isinstance(e, bankid.exceptions.BankIDError)


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
def test_error_class_factory(exception_class, error_code):
    from collections import namedtuple

    MockResponse = namedtuple("MockResponse", ["json"])
    response = MockResponse(json=lambda: {"errorCode": error_code})
    e_class = bankid.exceptions.get_json_error_class(response)
    assert isinstance(e_class, exception_class)
