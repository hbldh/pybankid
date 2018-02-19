#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

import bankid


@pytest.mark.parametrize("exception_class,rfa", [
    (bankid.exceptions.AccessDeniedRPError, None),
    (bankid.exceptions.AlreadyInProgressError, 3),
    (bankid.exceptions.CancelledError, 3),
    (bankid.exceptions.InvalidParametersError, None),
    (bankid.exceptions.InternalError, 5),
    (bankid.exceptions.RetryError, 5),
    (bankid.exceptions.ClientError, 12),
    (bankid.exceptions.ExpiredTransactionError, 8),
    (bankid.exceptions.CertificateError, 3),
    (bankid.exceptions.UserCancelError, 6),
    (bankid.exceptions.StartFailedError, 17),
])
def test_exceptions(exception_class, rfa):
    e = exception_class()
    assert e.rfa == rfa
    assert isinstance(e, bankid.exceptions.BankIDError)


@pytest.mark.parametrize("exception_class,message", [
    (bankid.exceptions.AccessDeniedRPError, 'ACCESS_DENIED_RP'),
    (bankid.exceptions.AlreadyInProgressError, 'ALREADY_IN_PROGRESS'),
    (bankid.exceptions.InvalidParametersError, 'INVALID_PARAMETERS'),
    (bankid.exceptions.InternalError, 'INTERNAL_ERROR'),
    (bankid.exceptions.RetryError, 'RETRY'),
    (bankid.exceptions.ClientError, 'CLIENT_ERR'),
    (bankid.exceptions.ExpiredTransactionError, 'EXPIRED_TRANSACTION'),
    (bankid.exceptions.CertificateError, 'CERTIFICATE_ERR'),
    (bankid.exceptions.UserCancelError, 'USER_CANCEL'),
    (bankid.exceptions.CancelledError, 'CANCELLED'),
    (bankid.exceptions.StartFailedError, 'START_FAILED'),
    (bankid.exceptions.BankIDError, 'Incorrect message string'),
])
def test_error_class_factory(exception_class, message):
    from collections import namedtuple
    nt = namedtuple('m', ['message', ])
    e_class = bankid.exceptions.get_error_class(nt(message=message), 'Test error')
    assert isinstance(e_class, exception_class)
