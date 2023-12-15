# This directory contains the root certificates used by BankID.
# We have to pin these to prevent basic MITM attacks.

from pathlib import Path


def get_test_cert_p12():
    return (Path(__file__).parent / "FPTestcert4_20230629.p12").resolve()


def get_test_cert_and_key():
    return (
        (Path(__file__).parent / "FPTestcert4_20230629_cert.pem").resolve(),
        (Path(__file__).parent / "FPTestcert4_20230629_key.pem").resolve(),
    )
