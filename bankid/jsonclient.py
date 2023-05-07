#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`bankid.jsonclient` -- BankID JSON Client
==============================================

Created on 2018-02-19 by hbldh

"""
import base64
from urllib import parse as urlparse

import requests
from pkg_resources import resource_filename

from bankid.exceptions import get_json_error_class


def _encode_user_data(user_data):
    if isinstance(user_data, str):
        return base64.b64encode(user_data.encode("utf-8")).decode("ascii")
    else:
        return base64.b64encode(user_data).decode("ascii")


class BankIDJSONClient(object):
    """The client to use for communicating with BankID servers via the v.5 API.

    :param certificates: Tuple of string paths to the certificate to use and
        the key to sign with.
    :type certificates: tuple
    :param test_server: Use the test server for authenticating and signing.
    :type test_server: bool
    :param request_timeout: Timeout for BankID requests.
    :type request_timeout: int

    """

    def __init__(self, certificates, test_server=False, request_timeout=None):
        self.certs = certificates
        self._request_timeout = request_timeout

        if test_server:
            self.api_url = "https://appapi2.test.bankid.com/rp/v5.1/"
            self.verify_cert = resource_filename("bankid.certs", "appapi2.test.bankid.com.pem")
        else:
            self.api_url = "https://appapi2.bankid.com/rp/v5.1/"
            self.verify_cert = resource_filename("bankid.certs", "appapi2.bankid.com.pem")

        self.client = requests.Session()
        self.client.verify = self.verify_cert
        self.client.cert = self.certs
        self.client.headers = {"Content-Type": "application/json"}

        self._auth_endpoint = urlparse.urljoin(self.api_url, "auth")
        self._sign_endpoint = urlparse.urljoin(self.api_url, "sign")
        self._collect_endpoint = urlparse.urljoin(self.api_url, "collect")
        self._cancel_endpoint = urlparse.urljoin(self.api_url, "cancel")

    def _post(self, endpoint, *args, **kwargs):
        """Internal helper method for adding timeout to requests."""
        return self.client.post(endpoint, *args, timeout=self._request_timeout, **kwargs)

    def authenticate(self, end_user_ip, personal_number=None, requirement=None, **kwargs):
        """Request an authentication order. The :py:meth:`collect` method
        is used to query the status of the order.

        Note that personal number is not needed when authentication is to
        be done on the same device, provided that the returned
        ``autoStartToken`` is used to open the BankID Client.

        Example data returned:

        .. code-block:: json

            {
                'orderRef': 'ee3421ea-2096-4000-8130-82648efe0927',
                'autoStartToken': 'e8df5c3c-c67b-4a01-bfe5-fefeab760beb',
                'qrStartToken': '01f94e28-857f-4d8a-bf8e-6c5a24466658',
                'qrStartSecret': 'b4214886-3b5b-46ab-bc08-6862fddc0e06'
            }

        :param end_user_ip: IP address of the user requesting
            the authentication.
        :type end_user_ip: str
        :param personal_number: The Swedish personal number in
            format YYYYMMDDXXXX.
        :type personal_number: str
        :param requirement: An optional dictionary stating how the signature
            must be created and verified. See BankID Relying Party Guidelines,
            section 13.5 for more details.
        :type requirement: dict
        :return: The order response.
        :rtype: dict
        :raises BankIDError: raises a subclass of this error
                             when error has been returned from server.

        """
        data = {"endUserIp": end_user_ip}
        if personal_number:
            data["personalNumber"] = personal_number
        if requirement and isinstance(requirement, dict):
            data["requirement"] = requirement
        # Handling potentially changed optional in-parameters.
        data.update(kwargs)
        response = self._post(self._auth_endpoint, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            raise get_json_error_class(response)

    def sign(
        self,
        end_user_ip,
        user_visible_data,
        personal_number=None,
        requirement=None,
        user_non_visible_data=None,
        **kwargs
    ):
        """Request a signing order. The :py:meth:`collect` method
        is used to query the status of the order.

        Note that personal number is not needed when signing is to be done
        on the same device, provided that the returned ``autoStartToken``
        is used to open the BankID Client.

        Example data returned:

        .. code-block:: json

            {
                'orderRef': 'ee3421ea-2096-4000-8130-82648efe0927',
                'autoStartToken': 'e8df5c3c-c67b-4a01-bfe5-fefeab760beb',
                'qrStartToken': '01f94e28-857f-4d8a-bf8e-6c5a24466658',
                'qrStartSecret': 'b4214886-3b5b-46ab-bc08-6862fddc0e06'
            }

        :param end_user_ip: IP address of the user requesting
            the authentication.
        :type end_user_ip: str
        :param user_visible_data: The information that the end user
            is requested to sign.
        :type user_visible_data: str
        :param personal_number: The Swedish personal number in
            format YYYYMMDDXXXX.
        :type personal_number: str
        :param requirement: An optional dictionary stating how the signature
            must be created and verified. See BankID Relying Party Guidelines,
            section 13.5 for more details.
        :type requirement: dict
        :param user_non_visible_data: Optional information sent with request
            that the user never sees.
        :type user_non_visible_data: str
        :return: The order response.
        :rtype: dict
        :raises BankIDError: raises a subclass of this error
                     when error has been returned from server.

        """
        data = {"endUserIp": end_user_ip}
        if personal_number:
            data["personalNumber"] = personal_number
        data["userVisibleData"] = _encode_user_data(user_visible_data)
        if user_non_visible_data:
            data["userNonVisibleData"] = _encode_user_data(user_non_visible_data)
        if requirement and isinstance(requirement, dict):
            data["requirement"] = requirement
        # Handling potentially changed optional in-parameters.
        data.update(kwargs)
        response = self._post(self._sign_endpoint, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            raise get_json_error_class(response)

    def collect(self, order_ref):
        """Collects the result of a sign or auth order using the
        ``orderRef`` as reference.

        RP should keep on calling collect every two seconds as long as status
        indicates pending. RP must abort if status indicates failed. The user
        identity is returned when complete.

        Example collect results returned while authentication or signing is
        still pending:

        .. code-block:: json

            {
                "orderRef":"131daac9-16c6-4618-beb0-365768f37288",
                "status":"pending",
                "hintCode":"userSign"
            }

        Example collect result when authentication or signing has failed:

        .. code-block:: json

            {
                "orderRef":"131daac9-16c6-4618-beb0-365768f37288",
                "status":"failed",
                "hintCode":"userCancel"
            }

        Example collect result when authentication or signing is successful
        and completed:

        .. code-block:: json

            {
                "orderRef":"131daac9-16c6-4618-beb0-365768f37288",
                "status":"complete",
                "completionData": {
                    "user": {
                        "personalNumber":"190000000000",
                        "name":"Karl Karlsson",
                        "givenName":"Karl",
                        "surname":"Karlsson"
                    },
                    "device": {
                        "ipAddress":"192.168.0.1"
                    },
                    "cert": {
                        "notBefore":"1502983274000",
                        "notAfter":"1563549674000"
                    },
                    "signature":"<base64-encoded data>",
                    "ocspResponse":"<base64-encoded data>"
                }
            }

        See `BankID Relying Party Guidelines Version: 3.5 <https://www.bankid.com/assets/bankid/rp/bankid-relying-party-guidelines-v3.5.pdf>`_
        for more details about how to inform end user of the current status,
        whether it is pending, failed or completed.

        :param order_ref: The ``orderRef`` UUID returned from auth or sign.
        :type order_ref: str
        :return: The CollectResponse parsed to a dictionary.
        :rtype: dict
        :raises BankIDError: raises a subclass of this error
                             when error has been returned from server.

        """
        response = self._post(self._collect_endpoint, json={"orderRef": order_ref})

        if response.status_code == 200:
            return response.json()
        else:
            raise get_json_error_class(response)

    def cancel(self, order_ref):
        """Cancels an ongoing sign or auth order.

        This is typically used if the user cancels the order
        in your service or app.

        :param order_ref: The UUID string specifying which order to cancel.
        :type order_ref: str
        :return: Boolean regarding success of cancellation.
        :rtype: bool
        :raises BankIDError: raises a subclass of this error
                             when error has been returned from server.

        """
        response = self._post(self._cancel_endpoint, json={"orderRef": order_ref})

        if response.status_code == 200:
            return response.json() == {}
        else:
            raise get_json_error_class(response)
