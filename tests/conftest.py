#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import requests

import bankid
from bankid.certs import get_test_cert_and_key


@pytest.fixture(scope="module")
def ip_address():
    return requests.get("https://httpbin.org/ip").json()["origin"].split(",")[0]


@pytest.fixture(scope="session")
def cert_and_key(tmpdir_factory):
    cert, key = get_test_cert_and_key()
    return cert, key
