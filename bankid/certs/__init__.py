# This directory contains the root certificates used by BankID.
# We have to pin these to prevent basic MITM attacks.

from pathlib import Path
from typing import Tuple


def get_test_cert_p12() -> Path:
    return (Path(__file__).parent / "FPTestcert5_20240610.p12").resolve()


def get_test_cert_and_key() -> Tuple[Path, Path]:
    return (
        (Path(__file__).parent / "FPTestcert5_20240610_cert.pem").resolve(),
        (Path(__file__).parent / "FPTestcert5_20240610_key.pem").resolve(),
    )
