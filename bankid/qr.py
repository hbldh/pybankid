from typing import Union

import hashlib
import hmac
import time
from datetime import datetime
from math import floor


def generate_qr_code_content(qr_start_token: str, start_t: Union[float, datetime], qr_start_secret: str) -> str:
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
