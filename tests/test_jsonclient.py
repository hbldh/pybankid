import pytest

import bankid


@pytest.mark.parametrize(
    "test_server, endpoint",
    [(False, "appapi2.bankid.com"), (True, "appapi2.test.bankid.com")],
)
def test_correct_prod_server_urls(cert_and_key, test_server, endpoint):
    c = bankid.BankIDJSONClient(certificates=cert_and_key, test_server=test_server)
    assert c.api_url == "https://{0}/rp/v5.1/".format(endpoint)
    assert "{0}.pem".format(endpoint) in c.verify_cert
