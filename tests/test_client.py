#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`test_client`
==================

.. module:: test_client
   :platform: Unix, Windows
   :synopsis: 

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2015-08-07, 12:00

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import tempfile
import uuid

import bankid.client
import bankid.testcert


class TestClient(object):

    def __init__(self):
        self.cert_file = None
        self.key_file = None

    def setUp(self):
        certificate, key = bankid.testcert.split_test_cert_and_key()

        self.cert_file = tempfile.NamedTemporaryFile(suffix='.pem', mode='wt', delete=False)
        self.cert_file.write(certificate)
        self.cert_file.close()
        print(self.cert_file.name)
        self.key_file = tempfile.NamedTemporaryFile(suffix='.pem', mode='wt', delete=False)
        self.key_file.write(certificate)
        self.key_file.close()
        print(self.key_file.name)

    def tearDown(self):
        try:
            os.remove(self.cert_file)
            os.remove(self.key_file)
        except:
            pass

    def test_connectivity(self):
        c = bankid.client.BankIDClient(certificates=(self.cert_file.name, self.key_file.name), test_server=True)
        ut = c.authenticate('197001010000')
        val = uuid.UUID(ut.get('orderRef'), version=4)
