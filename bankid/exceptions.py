#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`bankid.exceptions` -- PyBankID Exceptions
===============================================

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2014-09-10, 08:29

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import six


def get_error_class(exc, exception_text):
    error_class = _ERROR_CODE_TO_CLASS.get(six.text_type(exc.message))
    if error_class is None:
        return BankIDError("{0}: {1}".format(exc, exception_text))
    else:
        return error_class(exception_text)


def get_json_error_class(response):
    data = response.json()
    error_class = _JSON_ERROR_CODE_TO_CLASS.get(
        data.get('errorCode'), BankIDError)
    return error_class("{0}: {1}".format(
        data.get('errorCode'), data.get("details")))


class BankIDError(Exception):
    """Parent exception class for all PyBankID errors."""

    def __init__(self, *args, **kwargs):
        super(BankIDError, self).__init__(*args, **kwargs)
        self.rfa = None


class BankIDWarning(Warning):
    """Warning class for PyBankID."""
    pass


class InvalidParametersError(BankIDError):
    """User induced error.

    **Code:** ``INVALID_PARAMETERS``

    **Reason:** Invalid parameter. Invalid use of method.

    **Action by RP:** RP must not try the same request again.
    This is an internal error within RP's system and must not be '
    communicated to the user as a BankID error.

    """


class AlreadyInProgressError(BankIDError):
    """Failure to create new order due to one already in progress.

    **Code:** ``ALREADY_IN_PROGRESS``

    **Reason:** An order for this user is already in progress. The order
    is aborted. No order is created.

    **Action by RP:** RP must inform the user that a login or signing
    operation is already initiated for this user.
    Message RFA3 should be used.

    """

    def __init__(self, *args, **kwargs):
        super(AlreadyInProgressError, self).__init__(*args, **kwargs)
        self.rfa = 3


class InternalError(BankIDError):
    """Remote server error.

    **Code:** ``INTERNAL_ERROR``

    **Reason:** Internal technical error in the BankID system.

    **Action by RP:** RP must not automatically try again. RP must
    inform the user that a technical error has
    occurred. Message RFA5 should be used.

    """

    def __init__(self, *args, **kwargs):
        super(InternalError, self).__init__(*args, **kwargs)
        self.rfa = 5


class MaintenanceError(BankIDError):
    """The service is temporarily out of service.

    **Action by RP:** RP may try again without informing the user.
    If this error is returned repeatedly, RP must inform the user.
    Message RFA5.

    """

    def __init__(self, *args, **kwargs):
        super(MaintenanceError, self).__init__(*args, **kwargs)
        self.rfa = 5


class RetryError(BankIDError):
    """Remote server error, different from InternalError.

    **Code:** ``RETRY``

    **Reason:** Internal technical error in the BankID system.

    **Action by RP:** RP must not automatically try again. RP must
    inform the user that a technical error has
    occurred. Message RFA5 should be used.

    """

    def __init__(self, *args, **kwargs):
        super(RetryError, self).__init__(*args, **kwargs)
        self.rfa = 5


class AccessDeniedRPError(BankIDError):
    """Access permission denied error.

    **Code:** ``ACCESS_DENIED_RP``

    **Reason:** RP does not have access to the service or
    requested operation.

    **Action by RP:** RP must not try the same request again. This is
    an internal error within RP's system and must
    not be communicated to the user as a BankID-error.

    """


class ClientError(BankIDError):
    """Remote technical error.

    **Code:** ``CLIENT_ERR``

    **Reason:** Internal technical error. It was not possible to
    create or verify the transaction.

    **Action by RP:** RP must not automatically try again. RP must
    inform the user. Message RFA12.

    """

    def __init__(self, *args, **kwargs):
        super(ClientError, self).__init__(*args, **kwargs)
        self.rfa = 12


class ExpiredTransactionError(BankIDError):
    """Error due to collecting on an expired order.

    **Code:** ``EXPIRED_TRANSACTION``

    **Reason:** The order has expired. The BankID security
    app/program did not start, the user did not
    finalize the signing or the RP called collect
    too late.

    **Action by RP:** RP must inform the user. Message RFA8.

    """

    def __init__(self, *args, **kwargs):
        super(ExpiredTransactionError, self).__init__(*args, **kwargs)
        self.rfa = 8


class CertificateError(BankIDError):
    """Error due to certificate issues.

    **Code:** ``CERTIFICATE_ERR``

    **Reason:**
    This error is returned if:
        1) The user has entered wrong security code
           too many times in her mobile device. The
           Mobile BankID cannot be used.
        2) The users BankID is revoked.
        3) The users BankID is invalid.

    **Action by RP:** RP must inform the user. Message RFA3.

    """

    def __init__(self, *args, **kwargs):
        super(CertificateError, self).__init__(*args, **kwargs)
        self.rfa = 3


class UserCancelError(BankIDError):
    """User had issue a cancel on the order.

    **Code:** ``USER_CANCEL``

    **Reason:** The user decided to cancel the order.

    **Action by RP:** RP must inform the user. Message RFA6.

    """

    def __init__(self, *args, **kwargs):
        super(UserCancelError, self).__init__(*args, **kwargs)
        self.rfa = 6


class CancelledError(BankIDError):
    """User had issue a cancel on the order.

    **Code:** ``CANCELLED``

    **Reason:** The order was cancelled. The system
    received a new order for the user.

    **Action by RP:** RP must inform the user. Message RFA3.

    """

    def __init__(self, *args, **kwargs):
        super(CancelledError, self).__init__(*args, **kwargs)
        self.rfa = 3


class StartFailedError(BankIDError):
    """Error handling the order's progression due to RP/user issues.

    **Code:** ``START_FAILED``

    **Reason:** The user did not provide her ID, or the RP
    requires ``autostarttoken`` to be used, but the
    client did not start within a certain time limit.
    The reason may be:

        1) RP did not use autoStartToken when starting
           BankID security program/app.
        2) The client software was not installed
           or other problem with the user’s computer.

    **Action by RP:**

        1) The RP must use autoStartToken when
           starting the client.
        2) The RP must inform the user. Message RFA17.

    """

    def __init__(self, *args, **kwargs):
        super(StartFailedError, self).__init__(*args, **kwargs)
        # TODO: Dual cause, in which only one requires RFA. Remove?
        self.rfa = 17


class UnauthorizedError(BankIDError):
    """RP does not have access to the service.

    **Action by RP:** RP must not try the same request again.
    This is an internal error within RP's system and must not be '
    communicated to the user as a BankID error.

    """
    pass


class NotFoundError(BankIDError):
    """An erroneously URL path was used.

    **Action by RP:** RP must not try the same request again.
    This is an internal error within RP's system and must not be '
    communicated to the user as a BankID error.

    """
    pass


class RequestTimeoutError(BankIDError):
    """It took too long time to transmit the request.

    **Action by RP:** RP must not automatically try again.
    This error may occur if the processing at RP or the communication is too
    slow. RP must inform the user. Message RFA5

    """
    def __init__(self, *args, **kwargs):
        super(RequestTimeoutError, self).__init__(*args, **kwargs)
        self.rfa = 5


_ERROR_CODE_TO_CLASS = {
    'INVALID_PARAMETERS': InvalidParametersError,
    'ALREADY_IN_PROGRESS': AlreadyInProgressError,
    'INTERNAL_ERROR': InternalError,
    'RETRY': RetryError,
    'ACCESS_DENIED_RP': AccessDeniedRPError,
    'CLIENT_ERR': ClientError,
    'EXPIRED_TRANSACTION': ExpiredTransactionError,
    'CERTIFICATE_ERR': CertificateError,
    'USER_CANCEL': UserCancelError,
    'CANCELLED': CancelledError,
    'START_FAILED': StartFailedError,
}


_JSON_ERROR_CODE_TO_CLASS = {
    'invalidParameters': InvalidParametersError,
    'alreadyInProgress': AlreadyInProgressError,
    'unauthorized': UnauthorizedError,
    'notFound': NotFoundError,
    'requestTimeout': RequestTimeoutError,
    # 'unsupportedMediaType': ,  # This will not be handled here...
    'internalError': InternalError,
    'Maintenance': MaintenanceError
}
