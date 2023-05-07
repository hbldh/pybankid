import base64
import xml.etree.ElementTree as ET
from textwrap import wrap

make_cert = lambda e: "-----BEGIN CERTIFICATE-----\n" + "\n".join(wrap(e, 54)) + "\n-----END CERTIFICATE-----"


class B64Value:
    def __init__(self, value):
        self.value = value

    @property
    def decode(self):
        return base64.b64decode(self.value)

    def raw(self):
        return self.value

    def __str__(self):
        return self.raw()


class BankIdSignatureContainer:
    def __init__(self, signature):
        self.root = ET.fromstring(signature.decode)
        self.raw = signature

    @property
    def signature_value(self):
        return B64Value(self.root[1].text).decode

    @property
    def signed_data_digest(self):
        return self.root[0][2][2]

    @property
    def key_data_digest(self):
        return self.root[0][3][2]

    @property
    def signature_value(self):
        return self.root[1]

    @property
    def signed_data_raw(self):
        return self.root[3][0]

    @property
    def certificates(self):
        return [e for e in self.root[2][0]]

    @property
    def bid_signed_data_raw(self):
        raw_xml_string = self.raw.decode.decode()
        start = raw_xml_string.find("<Object>") + len("<Object>")
        stop = raw_xml_string.find("</Object>")
        return raw_xml_string[start:stop]

    @property
    def user_non_visible_data(self):
        return self.root[3][0][1].text

    @property
    def signed_info(self):
        raw_xml_string = self.raw.decode.decode()
        start = raw_xml_string.find("<SignedInfo")
        stop = raw_xml_string.find("</SignedInfo>")
        return raw_xml_string[start:stop] + "</SignedInfo>"

    @property
    def key_info_raw(self):
        raw_xml_string = self.raw.decode.decode()
        start = raw_xml_string.find("<KeyInfo")
        stop = raw_xml_string.find("</KeyInfo>")
        return raw_xml_string[start:stop] + "</KeyInfo>"

    @property
    def server_info(self):
        return {
            "name": B64Value(self.root[3][0][2][0].text).decode,
            "displayName": B64Value(self.root[3][0][2][2].text).decode,
        }


class CompletionDataContainer:
    def __init__(self, completion_data):
        self.completion_data = completion_data

    @property
    def order_ref(self):
        return self.completion_data["orderRef"]

    @property
    def ocsp_response(self):
        return self.completion_data["ocspResponse"]

    @property
    def device(self):
        return self.completion_data["device"]

    @property
    def user(self):
        return self.completion_data["user"]

    @property
    def signature(self):
        return B64Value(self.completion_data["signature"])

    @property
    def signature_container(self):
        return BankIdSignatureContainer(self.signature)


class NonceParse:
    def __init__(self, bytes):
        self.bytes = bytes

    @property
    def type(self):
        return ".".join(str(e) for e in list(self.bytes.contents[2:11]))

    @property
    def critical(self):
        return self.bytes.contents[13] == 255

    @property
    def value(self):
        return self.bytes[16:]
