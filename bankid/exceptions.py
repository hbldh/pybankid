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


def get_json_error_class(response):
    data = response.json()
    error_class = _JSON_ERROR_CODE_TO_CLASS.get(data.get("errorCode"), BankIDError)
    return error_class("{0}: {1}".format(data.get("errorCode"), data.get("details")))


class BankIDError(Exception):
    """Parent exception class for all PyBankID errors.
    
    If an unknown error code is returned, RP should inform the user. 
    Message RFA22 should be used. RP should update their implementation
    to support the new error code as soon as possible. 
    """

    RFA = 22


class BankIDWarning(Warning):
    """Warning class for PyBankID."""

    pass


class InvalidParametersError(BankIDError):
    """
    **errorCode:** ``invalidParameters``

    **Reason:** Invalid parameter. Invalid use of method.

    **Action by RP:** RP must not try the same request again.
    This is an internal error within RP's system and must not be '
    communicated to the user as a BankID error.

    """

    RFA = None


class AlreadyInProgressError(BankIDError):
    """
    **errorCode:** ``alreadyInProgress``

    **Reason:** An order for this user is already in progress. The order
    is aborted. No order is created.

    **Action by RP:** RP must inform the user that a login or signing
    operation is already initiated for this user.
    Message RFA4 should be used.

    """

    RFA = 4


class InternalError(BankIDError):
    """
    **errorCode:** ``internalError``

    **Reason:** Internal technical error in the BankID system.

    **Action by RP:** RP must not automatically try again. RP must
    inform the user that a technical error has
    occurred. Message RFA5 should be used.

    """

    RFA = 5


class MaintenanceError(BankIDError):
    """
    **errorCode:** ``Maintenance``

    **Reason:** The service is temporarily out of service.

    **Action by RP:** RP may try again without informing the user.
    If this error is returned repeatedly, RP must inform the user.
    Message RFA5.

    """

    RFA = 5


class UnauthorizedError(BankIDError):
    """
    **errorCode:** ``unauthorized``

    **Reason:** RP does not have access to the service.

    **Action by RP:** RP must not try the same request again.
    This is an internal error within RP's system and must not be '
    communicated to the user as a BankID error.

    """

    RFA = None


class NotFoundError(BankIDError):
    """
    **errorCode:** ``notFound```
    
    **Reason:** An erroneously URL path was used.

    **Action by RP:** RP must not try the same request again.
    This is an internal error within RP's system and must not be '
    communicated to the user as a BankID error.

    """

    RFA = None


class RequestTimeoutError(BankIDError):
    """
    **errorCode:** ``requestTimeout``
    
    **Reason:** It took too long time to transmit the request.

    **Action by RP:** RP must not automatically try again.
    This error may occur if the processing at RP or the communication is too
    slow. RP must inform the user. Message RFA5

    """

    RFA = 5


_JSON_ERROR_CODE_TO_CLASS = {
    "invalidParameters": InvalidParametersError,
    "alreadyInProgress": AlreadyInProgressError,
    "unauthorized": UnauthorizedError,
    "notFound": NotFoundError,
    "requestTimeout": RequestTimeoutError,
    # 'unsupportedMediaType': ,  # This will not be handled here...
    "internalError": InternalError,
    "Maintenance": MaintenanceError,
}
