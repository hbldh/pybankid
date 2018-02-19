#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tempfile

import pytest
import requests

import bankid


@pytest.fixture(scope="module")
def ip_address():
    return requests.get("https://httpbin.org/ip").json()['origin']


@pytest.fixture(scope="session")
def cert_and_key():
    cert, key = bankid.create_bankid_test_server_cert_and_key(
        tempfile.gettempdir())
    return cert, key
