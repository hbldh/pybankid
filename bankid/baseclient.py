import base64
from datetime import datetime
from typing import Tuple, Dict, Any, Union, TypeVar, Generic
from urllib.parse import urljoin

from bankid.qr import generate_qr_code_content
from bankid.certutils import resolve_cert_path

import httpx

TClient = TypeVar("TClient", httpx.AsyncClient, httpx.Client)


class BankIDClientBaseclass(Generic[TClient]):
    """Baseclass for BankID clients.

    Both the synchronous and asynchronous clients inherit from this base class and has the methods implemented here.
    """

    client: TClient

    def __init__(
        self,
        certificates: Tuple[str, str],
        test_server: bool = False,
        request_timeout: int = 5,
    ):
        self.certs = certificates

        if test_server:
            self.api_url = "https://appapi2.test.bankid.com/rp/v6.0/"
            self.verify_cert = resolve_cert_path("appapi2.test.bankid.com.pem")
        else:
            self.api_url = "https://appapi2.bankid.com/rp/v6.0/"
            self.verify_cert = resolve_cert_path("appapi2.bankid.com.pem")

        self._auth_endpoint = urljoin(self.api_url, "auth")
        self._phone_auth_endpoint = urljoin(self.api_url, "phone/auth")
        self._sign_endpoint = urljoin(self.api_url, "sign")
        self._phone_sign_endpoint = urljoin(self.api_url, "phone/sign")
        self._collect_endpoint = urljoin(self.api_url, "collect")
        self._cancel_endpoint = urljoin(self.api_url, "cancel")

    @staticmethod
    def generate_qr_code_content(qr_start_token: str, start_t: Union[float, datetime], qr_start_secret: str) -> str:
        return generate_qr_code_content(qr_start_token, start_t, qr_start_secret)

    @staticmethod
    def _encode_user_data(user_data: str) -> str:
        return base64.b64encode(user_data.encode("utf-8")).decode("ascii")

    def _create_payload(
        self,
        end_user_ip: Union[str, None] = None,
        requirement: Union[Dict[str, Any], None] = None,
        user_visible_data: Union[str, None] = None,
        user_non_visible_data: Union[str, None] = None,
        user_visible_data_format: Union[str, None] = None,
    ) -> Dict[str, str]:
        data: Dict[str, Any] = {}
        if end_user_ip:
            data["endUserIp"] = end_user_ip
        if requirement and isinstance(requirement, dict):
            data["requirement"] = requirement
        if user_visible_data:
            data["userVisibleData"] = self._encode_user_data(user_visible_data)
        if user_non_visible_data:
            data["userNonVisibleData"] = self._encode_user_data(user_non_visible_data)
        if user_visible_data_format and user_visible_data_format == "simpleMarkdownV1":
            data["userVisibleDataFormat"] = "simpleMarkdownV1"
        return data
