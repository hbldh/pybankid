import os

from pytest import TempdirFactory

import bankid


def test_create_bankid_test_server_cert_and_key(tmpdir_factory: TempdirFactory) -> None:
    paths = bankid.certutils.create_bankid_test_server_cert_and_key(tmpdir_factory.mktemp("certs"))
    assert os.path.exists(paths[0])
    assert os.path.exists(paths[1])
    try:
        os.remove(paths[0])
        os.remove(paths[1])
    except Exception:
        pass
