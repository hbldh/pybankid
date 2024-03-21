import base64
from datetime import datetime
import hashlib
import hmac
from math import floor
import time
from typing import Tuple, Optional, Dict, Any
from urllib.parse import urljoin

from bankid.certutils import resolve_cert_path


class BankIDClientBaseclass:
    """Baseclass for BankID clients."""

    def __init__(
        self,
        certificates: Tuple[str, str],
        test_server: bool = False,
        request_timeout: Optional[int] = None,
    ):
        self.certs = certificates
        self._request_timeout = request_timeout

        if test_server:
            self.api_url = "https://appapi2.test.bankid.com/rp/v6.0/"
            self.verify_cert = resolve_cert_path("appapi2.test.bankid.com.pem")
        else:
            self.api_url = "https://appapi2.bankid.com/rp/v6.0/"
            self.verify_cert = resolve_cert_path("appapi2.bankid.com.pem")

        self._auth_endpoint = urljoin(self.api_url, "auth")
        self._sign_endpoint = urljoin(self.api_url, "sign")
        self._collect_endpoint = urljoin(self.api_url, "collect")
        self._cancel_endpoint = urljoin(self.api_url, "cancel")

        self.client = None

    @staticmethod
    def _encode_user_data(user_data):
        if isinstance(user_data, str):
            return base64.b64encode(user_data.encode("utf-8")).decode("ascii")
        else:
            return base64.b64encode(user_data).decode("ascii")

    @staticmethod
    def generate_qr_code_content(qr_start_token: str, start_t: [float, datetime], qr_start_secret: str):
        """Given QR start token, time.time() or UTC datetime when initiated authentication call was made and the
        QR start secret, calculate the current QR code content to display.
        """
        if isinstance(start_t, datetime):
            start_t = start_t.timestamp()
        elapsed_seconds_since_call = int(floor(time.time() - start_t))
        qr_auth_code = hmac.new(
            qr_start_secret.encode(),
            msg=str(elapsed_seconds_since_call).encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()
        return f"bankid.{qr_start_token}.{elapsed_seconds_since_call}.{qr_auth_code}"

    def _create_payload(
        self,
        end_user_ip: str,
        requirement: Dict[str, Any] = None,
        user_visible_data: str = None,
        user_non_visible_data: str = None,
        user_visible_data_format: str = None,
    ):
        data = {"endUserIp": end_user_ip}
        if requirement and isinstance(requirement, dict):
            data["requirement"] = requirement
        if user_visible_data:
            data["userVisibleData"] = self._encode_user_data(user_visible_data)
        if user_non_visible_data:
            data["userNonVisibleData"] = self._encode_user_data(user_non_visible_data)
        if user_visible_data_format and user_visible_data_format == "simpleMarkdownV1":
            data["userVisibleDataFormat"] = "simpleMarkdownV1"
        return data
