#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`bankid.exceptions` -- PyBankID Exceptions
===============================================

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2014-09-10, 08:29

"""


def get_json_error_class(response):
    data = response.json()
    error_class = _JSON_ERROR_CODE_TO_CLASS.get(data.get("errorCode"), BankIDError)
    return error_class("{0}: {1}".format(data.get("errorCode"), data.get("details")))


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

    **Code:** ``invalidParameters``

    **Reason:** Invalid parameter. Invalid use of method.

    **Action by RP:** RP must not try the same request again.
    This is an internal error within RP's system and must not be '
    communicated to the user as a BankID error.

    """


class AlreadyInProgressError(BankIDError):
    """Failure to create new order due to one already in progress.

    **Code:** ``alreadyInProgress``

    **Reason:** An order for this user is already in progress. The order
    is aborted. No order is created.

    **Action by RP:** RP must inform the user that a login or signing
    operation is already initiated for this user.
    Message RFA4 should be used.

    """

    def __init__(self, *args, **kwargs):
        super(AlreadyInProgressError, self).__init__(*args, **kwargs)
        self.rfa = 4


class InternalError(BankIDError):
    """Remote server error.

    **Code:** ``internalError``

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

    **Code:** ``maintenance``

    **Action by RP:** RP may try again without informing the user.
    If this error is returned repeatedly, RP must inform the user.
    Message RFA5.

    """

    def __init__(self, *args, **kwargs):
        super(MaintenanceError, self).__init__(*args, **kwargs)
        self.rfa = 5


class UnauthorizedError(BankIDError):
    """RP does not have access to the service.

    **Code:** ``unauthorized``

    **Action by RP:** RP must not try the same request again.
    This is an internal error within RP's system and must not be '
    communicated to the user as a BankID error.

    """

    pass


class NotFoundError(BankIDError):
    """An erroneously URL path was used.

    **Code:** ``notFound``

    **Action by RP:** RP must not try the same request again.
    This is an internal error within RP's system and must not be '
    communicated to the user as a BankID error.

    """

    pass


class RequestTimeoutError(BankIDError):
    """It took too long time to transmit the request.

    **Code:** ``requestTimeout``

    **Action by RP:** RP must not automatically try again.
    This error may occur if the processing at RP or the communication is too
    slow. RP must inform the user. Message RFA5

    """

    def __init__(self, *args, **kwargs):
        super(RequestTimeoutError, self).__init__(*args, **kwargs)
        self.rfa = 5


_JSON_ERROR_CODE_TO_CLASS = {
    "invalidParameters": InvalidParametersError,
    "alreadyInProgress": AlreadyInProgressError,
    "unauthorized": UnauthorizedError,
    "notFound": NotFoundError,
    # 'methodNotAllowed': ,  # This will not be handled here...
    "requestTimeout": RequestTimeoutError,
    # 'unsupportedMediaType': ,  # This will not be handled here...
    "internalError": InternalError,
    "maintenance": MaintenanceError,
}
