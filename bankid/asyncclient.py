from typing import Any, Dict, Tuple, Union

import httpx

from bankid.baseclient import BankIDClientBaseclass
from bankid.exceptions import get_json_error_class


class BankIDAsyncClient(BankIDClientBaseclass[httpx.AsyncClient]):
    """The asynchronous client to use for communicating with BankID servers via the v6 API.

    :param certificates: Tuple of string paths to the certificate to use and
        the key to sign with.
    :type certificates: tuple
    :param test_server: Use the test server for authenticating and signing.
    :type test_server: bool
    :param request_timeout: Timeout for BankID requests.
    :type request_timeout: int

    """

    def __init__(self, certificates: Tuple[str, str], test_server: bool = False, request_timeout: int = 5):
        super().__init__(certificates, test_server, request_timeout)

        headers = {"Content-Type": "application/json"}
        self.client = httpx.AsyncClient(cert=self.certs, headers=headers, verify=str(self.verify_cert), timeout=request_timeout)

    async def authenticate(
        self,
        end_user_ip: str,
        requirement: Union[Dict[str, Any], None] = None,
        user_visible_data: Union[str, None]  = None,
        user_non_visible_data: Union[str, None]  = None,
        user_visible_data_format: Union[str, None]  = None,
    ) -> Dict[str, str]:
        """Request an authentication order. The :py:meth:`collect` method
        is used to query the status of the order.

        Example data returned:

        .. code-block:: json

            {
                "orderRef": "ee3421ea-2096-4000-8130-82648efe0927",
                "autoStartToken": "e8df5c3c-c67b-4a01-bfe5-fefeab760beb",
                "qrStartToken": "01f94e28-857f-4d8a-bf8e-6c5a24466658",
                "qrStartSecret": "b4214886-3b5b-46ab-bc08-6862fddc0e06"
            }

        :param end_user_ip: The user IP address as seen by RP. String. IPv4 and IPv6 is allowed.
        :type end_user_ip: str
        :param requirement: Requirements on how the auth order must be performed.
            See the section `Requirements <https://www.bankid.com/en/utvecklare/guider/teknisk-integrationsguide/graenssnittsbeskrivning/auth>`_ for more details.
        :type requirement: dict
        :param user_visible_data: Text displayed to the user during authentication with BankID,
            with the purpose of providing context for the authentication and to enable users
            to detect identification errors and averting fraud attempts.
        :type user_visible_data: str
        :param user_non_visible_data: Data is not displayed to the user.
        :type user_non_visible_data: str
        :param user_visible_data_format: If present, and set to “simpleMarkdownV1”,
            this parameter indicates that userVisibleData holds formatting characters which
            potentially make for a more pleasant user experience.
        :type user_visible_data_format: str
        :return: The order response.
        :rtype: dict
        :raises BankIDError: raises a subclass of this error
                             when error has been returned from server.

        """
        data = self._create_payload(
            end_user_ip,
            requirement=requirement,
            user_visible_data=user_visible_data,
            user_non_visible_data=user_non_visible_data,
            user_visible_data_format=user_visible_data_format,
        )

        response = await self.client.post(self._auth_endpoint, json=data)

        if response.status_code == 200:
            return response.json()  # type: ignore[no-any-return]
        else:
            raise get_json_error_class(response)

    async def phone_authenticate(
        self,
        personal_number: str,
        call_initiator: str,
        requirement: Union[Dict[str, Any], None] = None,
        user_visible_data: Union[str, None] = None,
        user_non_visible_data: Union[str, None] = None,
        user_visible_data_format: Union[str, None] = None,
    ) -> Dict[str, str]:
        """Initiates an authentication order when the user is talking
        to the RP over the phone. The :py:meth:`collect` method
        is used to query the status of the order.

        Example data returned:

        .. code-block:: json

            {
                "orderRef": "ee3421ea-2096-4000-8130-82648efe0927"
            }

        :param personal_number: The personal number of the user. 12 digits.
        :type personal_number: str
        :param call_initiator: Indicate if the user or the RP initiated the phone call.
            "user": user called the RP
            "RP": RP called the user
        :type call_initiator: str
        :param requirement: Requirements on how the auth order must be performed.
            See the section `Requirements <https://www.bankid.com/en/utvecklare/guider/teknisk-integrationsguide/graenssnittsbeskrivning/phone-auth>`_ for more details.
        :type requirement: dict
        :param user_visible_data: Text displayed to the user during authentication with BankID,
            with the purpose of providing context for the authentication and to enable users
            to detect identification errors and averting fraud attempts.
        :type user_visible_data: str
        :param user_non_visible_data: Data is not displayed to the user.
        :type user_non_visible_data: str
        :param user_visible_data_format: If present, and set to “simpleMarkdownV1”,
            this parameter indicates that userVisibleData holds formatting characters which
            potentially make for a more pleasant user experience.
        :type user_visible_data_format: str
        :return: The order response.
        :rtype: dict
        :raises BankIDError: raises a subclass of this error
                             when error has been returned from server.

        """
        if call_initiator not in ["user", "RP"]:
            raise ValueError("call_initiator must be either 'user' or 'RP'")

        data = self._create_payload(
            requirement=requirement,
            user_visible_data=user_visible_data,
            user_non_visible_data=user_non_visible_data,
            user_visible_data_format=user_visible_data_format,
        )
        data["personalNumber"] = personal_number
        data["callInitiator"] = call_initiator

        response = await self.client.post(self._phone_auth_endpoint, json=data)

        if response.status_code == 200:
            return response.json()  # type: ignore[no-any-return]
        else:
            raise get_json_error_class(response)

    async def sign(
        self,
        end_user_ip: str,
        user_visible_data: str,
        requirement: Union[Dict[str, Any], None] = None,
        user_non_visible_data: Union[str, None] = None,
        user_visible_data_format: Union[str, None] = None,
    ) -> Dict[str, str]:
        """Request a signing order. The :py:meth:`collect` method
        is used to query the status of the order.

        Example data returned:

        .. code-block:: json

            {
                "orderRef": "ee3421ea-2096-4000-8130-82648efe0927",
                "autoStartToken": "e8df5c3c-c67b-4a01-bfe5-fefeab760beb",
                "qrStartToken": "01f94e28-857f-4d8a-bf8e-6c5a24466658",
                "qrStartSecret": "b4214886-3b5b-46ab-bc08-6862fddc0e06"
            }

        :param end_user_ip: The user IP address as seen by RP. String. IPv4 and IPv6 is allowed.
        :type end_user_ip: str
        :param requirement: Requirements on how the sign order must be performed.
            See the section `Requirements <https://www.bankid.com/en/utvecklare/guider/teknisk-integrationsguide/graenssnittsbeskrivning/sign>`_ for more details.
        :type requirement: dict
        :param user_visible_data: Text to be displayed to the user.
        :type user_visible_data: str
        :param user_non_visible_data: Data is not displayed to the user.
        :type user_non_visible_data: str
        :param user_visible_data_format: If present, and set to “simpleMarkdownV1”,
            this parameter indicates that userVisibleData holds formatting characters which
            potentially make for a more pleasant user experience.
        :type user_visible_data_format: str
        :return: The order response.
        :rtype: dict
        :raises BankIDError: raises a subclass of this error
                     when error has been returned from server.

        """
        data = self._create_payload(
            end_user_ip,
            requirement=requirement,
            user_visible_data=user_visible_data,
            user_non_visible_data=user_non_visible_data,
            user_visible_data_format=user_visible_data_format,
        )

        response = await self.client.post(self._sign_endpoint, json=data)

        if response.status_code == 200:
            return response.json()  # type: ignore[no-any-return]
        else:
            raise get_json_error_class(response)

    async def phone_sign(
        self,
        personal_number: str,
        call_initiator: str,
        user_visible_data: str,
        requirement: Union[Dict[str, Any], None] = None,
        user_non_visible_data: Union[str, None] = None,
        user_visible_data_format: Union[str, None] = None,
    ) -> Dict[str, str]:
        """Initiates an authentication order when the user is talking to
        the RP over the phone. The :py:meth:`collect` method
        is used to query the status of the order.

        Example data returned:

        .. code-block:: json

            {
                "orderRef": "ee3421ea-2096-4000-8130-82648efe0927"
            }

        :param personal_number: The personal number of the user. 12 digits.
        :type personal_number: str
        :param call_initiator: Indicate if the user or the RP initiated the phone call.
            "user": user called the RP
            "RP": RP called the user
        :type call_initiator: str
        :param requirement: Requirements on how the sign order must be performed.
            See the section `Requirements <https://www.bankid.com/en/utvecklare/guider/teknisk-integrationsguide/graenssnittsbeskrivning/sign>`_ for more details.
        :type requirement: dict
        :param user_visible_data: Text to be displayed to the user.
        :type user_visible_data: str
        :param user_non_visible_data: Data is not displayed to the user.
        :type user_non_visible_data: str
        :param user_visible_data_format: If present, and set to “simpleMarkdownV1”,
            this parameter indicates that userVisibleData holds formatting characters which
            potentially make for a more pleasant user experience.
        :type user_visible_data_format: str
        :return: The order response.
        :rtype: dict
        :raises BankIDError: raises a subclass of this error
                     when error has been returned from server.

        """
        if call_initiator not in ["user", "RP"]:
            raise ValueError("call_initiator must be either 'user' or 'RP'")

        data = self._create_payload(
            requirement=requirement,
            user_visible_data=user_visible_data,
            user_non_visible_data=user_non_visible_data,
            user_visible_data_format=user_visible_data_format,
        )
        data["personalNumber"] = personal_number
        data["callInitiator"] = call_initiator

        response = await self.client.post(self._phone_sign_endpoint, json=data)

        if response.status_code == 200:
            return response.json()  # type: ignore[no-any-return]
        else:
            raise get_json_error_class(response)

    async def collect(self, order_ref: str) -> dict:
        """Collects the result of a sign or auth order using the
        ``orderRef`` as reference.

        RP should keep on calling collect every two seconds if status is pending.
        RP must abort if status indicates failed. The user identity is returned
        when complete.

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
                "orderRef": "131daac9-16c6-4618-beb0-365768f37288",
                "status": "complete",
                "completionData": {
                    "user": {
                        "personalNumber": "190000000000",
                        "name": "Karl Karlsson",
                        "givenName": "Karl",
                        "surname": "Karlsson"
                    },
                    "device": {
                        "ipAddress": "192.168.0.1"
                    },
                    "bankIdIssueDate": "2020-02-01",
                    "signature": "<base64-encoded data>",
                    "ocspResponse": "<base64-encoded data>"
                }
            }

        See `BankID Integration Guide <https://www.bankid.com/en/utvecklare/guider/teknisk-integrationsguide/graenssnittsbeskrivning/collect>`_
        for more details about how to inform end user of the current status,
        whether it is pending, failed or completed.

        :param order_ref: The ``orderRef`` UUID returned from auth or sign.
        :type order_ref: str
        :return: The CollectResponse parsed to a dictionary.
        :rtype: dict
        :raises BankIDError: raises a subclass of this error
                             when error has been returned from server.

        """
        response = await self.client.post(self._collect_endpoint, json={"orderRef": order_ref})

        if response.status_code == 200:
            return response.json()  # type: ignore[no-any-return]
        else:
            raise get_json_error_class(response)

    async def cancel(self, order_ref: str) -> bool:
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
        response = await self.client.post(self._cancel_endpoint, json={"orderRef": order_ref})

        if response.status_code == 200:
            return response.json() == {}  # type: ignore[no-any-return]
        else:
            raise get_json_error_class(response)
