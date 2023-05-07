#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`bankid.certutils` -- Certificate Utilities
================================================

Created 2016-04-10 by hbldh

"""

import os
import subprocess

from bankid.certs import get_test_cert_p12
from bankid.exceptions import BankIDError

_TEST_CERT_PASSWORD = "qwerty123"
_TEST_CERT_URL = "https://www.bankid.com/assets/bankid/rp/FPTestcert4_20220818.p12"


def create_bankid_test_server_cert_and_key(destination_path):
    """Split the bundled test certificate into certificate and key parts and save them
    as separate files, stored in PEM format.

    If the environment variable TEST_CERT_FILE is set, use this file
    instead of fetching the P12 certificate.

    :param destination_path: The directory to save certificate and key files to.
    :type destination_path: str
    :returns: The path tuple ``(cert_path, key_path)``.
    :rtype: tuple

    """
    if os.getenv("TEST_CERT_FILE"):
        certificate, key = split_certificate(
            os.getenv("TEST_CERT_FILE"), destination_path, password=_TEST_CERT_PASSWORD
        )

    else:
        # Fetch testP12 certificate path
        certificate, key = split_certificate(str(get_test_cert_p12()), destination_path, password=_TEST_CERT_PASSWORD)

    # Return path tuples.
    return certificate, key


def split_certificate(certificate_path, destination_folder, password=None):
    """Splits a PKCS12 certificate into Base64-encoded DER certificate and key.

    This method splits a potentially password-protected
    `PKCS12 <https://en.wikipedia.org/wiki/PKCS_12>`_ certificate
    (format ``.p12`` or ``.pfx``) into one certificate and one key part, both in
    `pem <https://en.wikipedia.org/wiki/X.509#Certificate_filename_extensions>`_
    format.

    :returns: Tuple of certificate and key string data.
    :rtype: tuple

    """
    try:
        # Attempt Linux and Darwin call first.
        p = subprocess.Popen(["openssl", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sout, serr = p.communicate()
        openssl_executable_version = sout.decode().lower()
        if not (openssl_executable_version.startswith("openssl") or openssl_executable_version.startswith("libressl")):
            raise BankIDError("OpenSSL executable could not be found. " "Splitting cannot be performed.")
        openssl_executable = "openssl"
    except Exception:
        # Attempt to call on standard Git for Windows path.
        p = subprocess.Popen(
            ["C:\\Program Files\\Git\\mingw64\\bin\\openssl.exe", "version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        sout, serr = p.communicate()
        if not sout.decode().lower().startswith("openssl"):
            raise BankIDError("OpenSSL executable could not be found. " "Splitting cannot be performed.")
        openssl_executable = "C:\\Program Files\\Git\\mingw64\\bin\\openssl.exe"

    if not os.path.exists(os.path.abspath(os.path.expanduser(destination_folder))):
        os.makedirs(os.path.abspath(os.path.expanduser(destination_folder)))

    # Paths to output files.
    out_cert_path = os.path.join(os.path.abspath(os.path.expanduser(destination_folder)), "certificate.pem")
    out_key_path = os.path.join(os.path.abspath(os.path.expanduser(destination_folder)), "key.pem")

    # Use openssl for converting to pem format.
    pipeline_1 = [
        openssl_executable,
        "pkcs12",
        "-in",
        "{0}".format(certificate_path),
        "-passin" if password is not None else "",
        "pass:{0}".format(password) if password is not None else "",
        "-out",
        "{0}".format(out_cert_path),
        "-clcerts",
        "-nokeys",
    ]
    p = subprocess.Popen(list(filter(None, pipeline_1)), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    if p.returncode:
        raise BankIDError("Error converting certificate: {0}".format(err.decode("utf-8")))

    pipeline_2 = [
        openssl_executable,
        "pkcs12",
        "-in",
        "{0}".format(certificate_path),
        "-passin" if password is not None else "",
        "pass:{0}".format(password) if password is not None else "",
        "-out",
        "{0}".format(out_key_path),
        "-nocerts",
        "-nodes",
    ]
    p = subprocess.Popen(list(filter(None, pipeline_2)), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    if p.returncode:
        raise BankIDError("Error converting certificate: {0}".format(err.decode("utf-8")))

    # Return path tuples.
    return out_cert_path, out_key_path


def main(verbose=True):
    paths = create_bankid_test_server_cert_and_key(os.path.expanduser("~"))
    if verbose:
        print("Saved certificate as {0}".format(paths[0]))
        print("Saved key as {0}".format(paths[1]))
    return paths


if __name__ == "__main__":  # pragma: no cover
    main()
