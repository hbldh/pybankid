#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import bankid


def test_certutils_main():
    bankid.certutils.main(verbose=False)

    assert os.path.exists(os.path.expanduser('~/certificate.pem'))
    assert os.path.exists(os.path.expanduser('~/key.pem'))

    try:
        os.remove(os.path.expanduser('~/certificate.pem'))
        os.remove(os.path.expanduser('~/key.pem'))
    except:
        pass
