# This directory contains the root certificates used by BankID.
# We have to pin these to prevent basic MITM attacks.

from pathlib import Path


def get_test_cert_p12():
    return (Path(__file__).parent / "FPTestcert4_20220818.p12").resolve()
