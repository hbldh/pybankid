#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import requests

import bankid


@pytest.fixture(scope="module")
def ip_address():
    return requests.get("https://httpbin.org/ip").json()['origin']


@pytest.fixture(scope="session")
def cert_and_key(tmpdir_factory):
    testcert_dir = tmpdir_factory.mktemp('testcert')
    cert, key = bankid.create_bankid_test_server_cert_and_key(
        str(testcert_dir))
    return cert, key
