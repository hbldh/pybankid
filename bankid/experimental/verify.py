import base64
import datetime
import hashlib
from io import BytesIO
from logging import getLogger

import OpenSSL.crypto
import asn1crypto.ocsp
import pytz
from OpenSSL import crypto
from OpenSSL.crypto import X509StoreContextError
from asn1crypto import pem

from bankid.experimental.helper import CompletionDataContainer, make_cert, NonceParse

_LOG = getLogger(__name__)


def verify_bankid_response(bank_id_response, ensure_certificates_still_valid=True, BANK_ID_ROOT_CERT=None):

    if not isinstance(bank_id_response, dict):
        raise TypeError("Response not a dictionary")

    if "completionData" not in bank_id_response:
        raise AttributeError("Completion data missing in dictionary")

    try:
        cdc = CompletionDataContainer(bank_id_response["completionData"])

        # First step is to hash the data and verify the digest matches

        _LOG.info("1. Message Digest Verification\n")
        bid_signed_data_raw_bytes = cdc.signature_container.bid_signed_data_raw.encode()

        # TODO - Parse out of the XML which hashing algorithm should be sued

        bid_signed_data_hash = hashlib.sha256(bid_signed_data_raw_bytes).digest().hex()
        key_info_hash = hashlib.sha256(cdc.signature_container.key_info_raw.encode()).digest().hex()

        signed_data_hash_from_signature = base64.b64decode(cdc.signature_container.signed_data_digest.text).hex()
        key_info_hash_from_signature = base64.b64decode(cdc.signature_container.key_data_digest.text).hex()

        if bid_signed_data_hash != signed_data_hash_from_signature:
            raise AssertionError("Signed Data hash does not match!")

        if key_info_hash != key_info_hash_from_signature:
            raise AssertionError("Key Info hash does not match!")

        _LOG.info("\n2. Signature verification\n")

        # Helper function for the certificates
        user_certificate_string = make_cert(cdc.signature_container.certificates[0].text)

        # Making a certificate object out of it
        user_certificate = crypto.load_certificate(
            crypto.FILETYPE_PEM, BytesIO(user_certificate_string.encode()).read()
        )

        signature_bytes = base64.b64decode(cdc.signature_container.signature_value.text)
        signed_info = cdc.signature_container.signed_info.encode()

        try:
            _LOG.debug("Certificate:", user_certificate.get_subject())
            _LOG.debug("Signature Bytes:", signature_bytes)
            _LOG.debug("Signature Data Raw:", signed_info)

            OpenSSL.crypto.verify(user_certificate, signature_bytes, signed_info, "sha256")
        except OpenSSL.crypto.Error as e:
            raise AssertionError("The BankID signature is not valid!")

        _LOG.info("\n3. OCSP Response Verification\n")

        ocsp = base64.b64decode(bank_id_response["completionData"]["ocspResponse"])
        ocsp_response = asn1crypto.ocsp.OCSPResponse.load(ocsp)

        basic_ocsp_response = ocsp_response["response_bytes"]["response"].parsed

        # Some help by listing all the different parts of the OCSP response
        _LOG.debug("TBS Response Data", basic_ocsp_response["tbs_response_data"])
        _LOG.debug("SignatureAlgorithm", basic_ocsp_response["signature_algorithm"].signature_algo)
        _LOG.debug("SignatureAlgorithm Hash Function", basic_ocsp_response["signature_algorithm"].hash_algo)
        _LOG.debug("Signature", basic_ocsp_response["signature"].__bytes__())
        _LOG.debug("Cert", basic_ocsp_response["certs"])

        # Response content
        _LOG.debug("version", basic_ocsp_response["tbs_response_data"]["version"])
        _LOG.debug("responderID", basic_ocsp_response["tbs_response_data"]["responder_id"])  # has native
        _LOG.info("producedAt", basic_ocsp_response["tbs_response_data"]["produced_at"])

        cest = pytz.timezone("Europe/Stockholm")
        ocsp_produced_at = basic_ocsp_response["tbs_response_data"]["produced_at"].native

        if not isinstance(ocsp_produced_at, datetime.datetime):
            raise AssertionError("OCSP produced at is not a datetime!")

        ocsp_produced_at = ocsp_produced_at.astimezone(cest).strftime("%Y-%m-%d %H:%M:%S")

        _LOG.debug("responses", basic_ocsp_response["tbs_response_data"]["responses"])
        _LOG.debug("response Extentions", basic_ocsp_response["tbs_response_data"]["response_extensions"])

        _LOG.debug("Extentions")
        extention = basic_ocsp_response["tbs_response_data"]["response_extensions"][0]

        _LOG.debug("extn_id", extention["extn_id"])
        _LOG.debug("critical", extention["critical"])

        # Cannot _LOG.debug the value without an exception being raised - need to parse that ourself later
        # print ('extn_value', extention['extn_value'])

        single_response = basic_ocsp_response["tbs_response_data"]["responses"][0]

        _LOG.debug("CertID", single_response["cert_id"])
        _LOG.debug("certStatus", single_response["cert_status"])
        _LOG.debug("thisUpdate", single_response["this_update"])
        _LOG.debug("nextUpdate", single_response["next_update"])
        _LOG.debug("singleExtensions", single_response["single_extensions"])

        _LOG.info("3.1. OCSP Response - Verify success ")

        if ocsp_response["response_status"].native != "successful":
            raise AssertionError("OCSP response status was not successful")

        _LOG.info("3.2. OCSP Response - Verify signature ")

        # Transform the asn1 certificate to an openssl certificate
        der_bytes = basic_ocsp_response["certs"][0].dump()
        pem_bytes = pem.armor("CERTIFICATE", der_bytes)
        ocsp_certificate = crypto.load_certificate(crypto.FILETYPE_PEM, pem_bytes)

        # Get the signature bytes
        signature = basic_ocsp_response["signature"].__bytes__()

        # Dump the TBS response data as DER bytes
        signature_data = basic_ocsp_response["tbs_response_data"].dump()

        # Define the hashing algorithm to be used
        digest_method = basic_ocsp_response["signature_algorithm"].hash_algo

        _LOG.debug("Certificate", ocsp_certificate.get_subject())
        _LOG.debug("Signature", signature)
        _LOG.debug("Signature data", signature_data)
        _LOG.debug("Digest Method", digest_method)

        try:
            OpenSSL.crypto.verify(ocsp_certificate, signature, signature_data, digest_method)
        except OpenSSL.crypto.Error as e:
            raise AssertionError("The OCSP signature is not valid!")

        _LOG.info("3.2. OCSP Response - Compare nonce")

        nonce_computed = hashlib.sha1(bank_id_response["completionData"]["signature"].encode("utf-8")).digest().hex()

        # A helper because the asn1 library seems to have a problem with the nonce parsing in some form or the other
        nonce_parser = NonceParse(extention.contents)

        # Verify that the computed nonce is part of the nonce value given in the oscp
        # Note that it only partially matches as we use sha-1 to compute the hash

        _LOG.debug("Nonce value computed ", nonce_computed)
        _LOG.debug("Nonce value presented", nonce_parser.value.hex())

        if not nonce_parser.value.hex().startswith(nonce_computed):
            raise AssertionError("Computed nonce not matching the OCSP nonce")

        _LOG.info("\n4. Verify all the certificates by relying on the BankID root certificate as a trusted one \n")

        user_cert = crypto.load_certificate(
            crypto.FILETYPE_PEM, make_cert(cdc.signature_container.certificates[0].text).encode()
        )

        bank_user_cert = crypto.load_certificate(
            crypto.FILETYPE_PEM, make_cert(cdc.signature_container.certificates[1].text).encode()
        )

        bank_bank_id_cert = crypto.load_certificate(
            crypto.FILETYPE_PEM, make_cert(cdc.signature_container.certificates[2].text).encode()
        )

        bank_id_root_cert = crypto.load_certificate(crypto.FILETYPE_PEM, BANK_ID_ROOT_CERT.encode())

        # 3. verify the certificate chain of the tbs certificate

        # Make sure we respect or do not respect certificate expiration times
        if not ensure_certificates_still_valid:
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)

            bank_user_cert.set_notAfter(tomorrow.strftime("%Y%m%d%H%M%SZ").encode())
            bank_bank_id_cert.set_notAfter(tomorrow.strftime("%Y%m%d%H%M%SZ").encode())
            bank_id_root_cert.set_notAfter(tomorrow.strftime("%Y%m%d%H%M%SZ").encode())

            ocsp_certificate.set_notAfter(tomorrow.strftime("%Y%m%d%H%M%SZ").encode())
            user_cert.set_notAfter(tomorrow.strftime("%Y%m%d%H%M%SZ").encode())

        store = crypto.X509Store()
        store.add_cert(bank_user_cert)
        store.add_cert(bank_bank_id_cert)
        store.add_cert(bank_id_root_cert)

        try:
            # Verify the user certificate up to the root certificate
            store_ctx = crypto.X509StoreContext(store, user_cert)
            store_ctx.verify_certificate()
            _LOG.debug("User Certificate issued by the respective bank... OK")
        except X509StoreContextError:
            raise AssertionError("BankID user certificate chain could not be verified.")

        try:
            # Verify the ocsp certificate up to the root certificate
            store_ctx = crypto.X509StoreContext(store, ocsp_certificate)
            store_ctx.verify_certificate()
            _LOG.debug("OCSP Certificate issued by the respective bank... OK")
        except X509StoreContextError:
            raise AssertionError("OCSP certificate chain could not be verified.")

    except Exception as e:
        raise e

    return ocsp_produced_at
