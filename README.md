# PyBankID

![Build and Test](https://github.com/hbldh/pybankid/workflows/Build%20and%20Test/badge.svg)
![Documentation Status](https://readthedocs.org/projects/pybankid/badge/?version=latest)
![PyPI Version](https://img.shields.io/pypi/v/pybankid)
![PyPI License](https://img.shields.io/pypi/l/pybankid)

PyBankID is a client for providing BankID services as a Relying Party, i.e., providing authentication and signing functionality to end users. This package provides a simplifying interface for initiating authentication and signing orders and then collecting the results from the BankID servers.

The only supported BankID API version supported by PyBankID from version 1.0.0 is v6.0, which means that the Secure Start solution is the only supported way of providing BankID services. PyBankID versions prior to 1.0.0 will not work after 1st of May 2024.

If you intend to use PyBankID in your project, you are advised to read the [BankID Integration Guide](https://www.bankid.com/en/utvecklare/guider/teknisk-integrationsguide) before doing anything else. There, one can find information about how the BankID methods are defined and how to use them.

## Installation

PyBankID can be installed through pip:

```bash
pip install pybankid
```

## Usage

PyBankID provides both a synchronous and an asynchronous client for communication with BankID services. The example below will use the synchronous client, but the asynchronous client is used in an identical fashion, only using the `await` keyword before each function call.

### Synchronous client

```python
from bankid import BankIDClient
client = BankIDClient(certificates=(
    'path/to/certificate.pem',
    'path/to/key.pem',
))
```

Connection to the production server is the default in the client. If a test server is desired, send in the `test_server=True` keyword in the init of the client.

All authentication and signing calls require the end user's IP address to be included. An authentication order is initiated as such:

```python
client.authenticate(end_user_ip='194.168.2.25')
{
    'orderRef': 'ee3421ea-2096-4000-8130-82648efe0927',
    'autoStartToken': 'e8df5c3c-c67b-4a01-bfe5-fefeab760beb',
    'qrStartToken': '01f94e28-857f-4d8a-bf8e-6c5a24466658',
    'qrStartSecret': 'b4214886-3b5b-46ab-bc08-6862fddc0e06'
}
```

and a sign order is initiated in a similar fashion:

```python
client.sign(
    end_user_ip='194.168.2.25',
    user_visible_data="The information to sign."
)
{
    'orderRef': 'ee3421ea-2096-4000-8130-82648efe0927',
    'autoStartToken': 'e8df5c3c-c67b-4a01-bfe5-fefeab760beb',
    'qrStartToken': '01f94e28-857f-4d8a-bf8e-6c5a24466658',
    'qrStartSecret': 'b4214886-3b5b-46ab-bc08-6862fddc0e06'
}
```

If you want to ascertain that only one individual can authenticate or sign, you can specify this using the `requirement` keyword:

```python
client.sign(
   end_user_ip='194.168.2.25',
   user_visible_data="The information to sign."
   requirement={"personalNumber": "YYYYMMDDXXXX"}
)
{
    'orderRef': 'ee3421ea-2096-4000-8130-82648efe0927',
    'autoStartToken': 'e8df5c3c-c67b-4a01-bfe5-fefeab760beb',
    'qrStartToken': '01f94e28-857f-4d8a-bf8e-6c5a24466658',
    'qrStartSecret': 'b4214886-3b5b-46ab-bc08-6862fddc0e06'
}
```

If someone other than the one you specified tries to authenticate or sign, the BankID app will state that the request is not intended for the user.

The status of an order can then be studied by polling with the `collect` method using the received `orderRef`:

```python
client.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
{
    'hintCode': 'outstandingTransaction',
    'orderRef': 'a9b791c3-459f-492b-bf61-23027876140b',
    'status': 'pending'
}
```

```python
client.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
{
    'hintCode': 'userSign',
    'orderRef': 'a9b791c3-459f-492b-bf61-23027876140b',
    'status': 'pending'
}
```

```python
client.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
{
    'completionData': {
        'cert': {
            'notAfter': '1581289199000',
            'notBefore': '1518130800000'
        },
        'device': {
            'ipAddress': '0.0.0.0'
        },
        'ocspResponse': 'MIIHegoBAKCCB[...]',
        'signature': 'PD94bWwgdmVyc2lv[...]',
        'user': {
            'givenName': 'Namn',
            'name': 'Namn Namnsson',
            'personalNumber': 'YYYYMMDDXXXX',
            'surname': 'Namnsson'
        }
    },
    'orderRef': 'a9b791c3-459f-492b-bf61-23027876140b',
    'status': 'complete'
}
```

Please note that the `collect` method should be used sparingly: in the [BankID Integration Guide](https://www.bankid.com/en/utvecklare/guider/teknisk-integrationsguide) it is specified that _"collect should be called every two seconds and must not be called more frequent than once per second"_.

PyBankID also implements the `phone/auth` and `phone/sign` methods, for performing authentication and signing with
users that are contacted through phone. For documentation on this, see [PyBankID's Read the Docs page](https://pybankid.readthedocs.io/en/latest/).

### Asynchronous client

The asynchronous client is used in the same way as the synchronous client, with the difference that all request are performed asynchronously.

The synchronous guide above can be used as a reference for the asynchronous client as well, by simply adding the `await` keyword:

```python
from bankid import BankIDAsyncClient
client = BankIDAsyncClient(certificates=(
    'path/to/certificate.pem',
    'path/to/key.pem',
))

await client.authenticate(end_user_ip='194.168.2.25')
{
    'orderRef': 'ee3421ea-2096-4000-8130-82648efe0927',
    'autoStartToken': 'e8df5c3c-c67b-4a01-bfe5-fefeab760beb',
    'qrStartToken': '01f94e28-857f-4d8a-bf8e-6c5a24466658',
    'qrStartSecret': 'b4214886-3b5b-46ab-bc08-6862fddc0e06'
}
```

## PyBankID and QR codes

PyBankID can generate QR codes for you, and there is an example application in the [examples folder of the repo](https://github.com/hbldh/pybankid/tree/master/examples), where a Flask application called `qrdemo` shows one way to do authentication with animated QR codes.

The QR code content generation is done with the `generate_qr_code_content` method on the BankID Client instances, or directly
through the identically named method in `bankid.qr` module.

## Certificates

### Production certificates

If you want to use BankID in a production environment, then you will have to purchase this service from one of the [selling banks](https://www.bankid.com/foretag/anslut-foeretag). They will then provide you with a certificate that can be used to authenticate your company/application with the BankID servers.

This certificate has to be processed somewhat to be able to use with PyBankID, and how to do this depends on what the selling bank provides you with.

### Test certificate

The certificate to use when developing against the BankID test servers can be obtained through PyBankID:

```python
import os
import bankid
dir_to_save_cert_and_key_in = os.path.expanduser('~')
cert_and_key = bankid.create_bankid_test_server_cert_and_key(
    dir_to_save_cert_and_key_in)
print(cert_and_key)
['/home/hbldh/certificate.pem', '/home/hbldh/key.pem']
client = bankid.BankIDClient(
    certificates=cert_and_key, test_server=True)
```
