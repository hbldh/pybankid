#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`bankid.certutils` -- Certificate Utilities
================================================

Created by hbldh <henrik.blidh@nedomkull.com>

Created on 2016-04-10

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import tempfile
import subprocess
import requests

_TEST_CERT_PASSWORD = 'qwerty123'
_TEST_CERT_URL = "https://www.bankid.com/assets/bankid/rp/FPTestcert2_20150818_102329.pfx"


def create_bankid_test_server_cert_and_key(destination_path):
    """Fetch the P12 certificate from BankID servers, split it into
    a certificate part and a key part and save them as separate files,
    stored in PEM format.

    :param destination_path: The directory to save certificate and key files to.
    :type destination_path: str
    :returns: The path tuple ``(cert_path, key_path)``.
    :rtype: tuple

    """

    # Fetch P12 certificate and store in temporary folder.
    cert_tmp_path = os.path.join(tempfile.gettempdir(),
                                 os.path.basename(_TEST_CERT_URL))
    r = requests.get(_TEST_CERT_URL)
    with open(cert_tmp_path, 'wb') as f:
        f.write(r.content)

    certificate, key = split_certificate(cert_tmp_path,
                                         destination_path,
                                         password=_TEST_CERT_PASSWORD)
    # Try to remove temporary file.
    try:
        os.remove(cert_tmp_path)
    except:
        pass

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
        p = subprocess.Popen(["openssl", 'version'], stdout=subprocess.PIPE)
        sout, serr = p.communicate()
        if not sout.decode().lower().startswith('openssl'):
            raise NotImplementedError(
                "OpenSSL executable could not be found. "
                "Splitting cannot be performed.")
    except:
        raise NotImplementedError(
            "OpenSSL executable could not be found. "
            "Splitting cannot be performed.")

    # Paths to output files.
    out_cert_path = os.path.join(os.path.abspath(
        os.path.expanduser(destination_folder)), 'certificate.pem')
    out_key_path = os.path.join(os.path.abspath(
        os.path.expanduser(destination_folder)), 'key.pem')

    # Use openssl for converting to pem format.
    pipeline_1 = [
        'openssl', 'pkcs12',
        '-in', "{0}".format(certificate_path),
        '-passin' if password is not None else '',
        'pass:{0}'.format(password) if password is not None else '',
        '-out', "{0}".format(out_cert_path),
        '-clcerts', '-nokeys'
    ]
    p = subprocess.Popen(list(filter(None, pipeline_1)),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.communicate()
    pipeline_2 = [
        'openssl', 'pkcs12',
        '-in', "{0}".format(certificate_path),
        '-passin' if password is not None else '',
        'pass:{0}'.format(password) if password is not None else '',
        '-out', "{0}".format(out_key_path),
        '-nocerts', '-nodes'
    ]
    p = subprocess.Popen(list(filter(None, pipeline_2)),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.communicate()

    # Return path tuples.
    return out_cert_path, out_key_path


def main():
    paths = create_bankid_test_server_cert_and_key(os.path.expanduser('~'))
    print('Saved certificate as {0}'.format(paths[0]))
    print('Saved key as {0}'.format(paths[1]))
    return paths

if __name__ == "__main__":
    main()
