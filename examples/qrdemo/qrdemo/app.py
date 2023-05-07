import pathlib
import time
from math import floor
import hmac
import hashlib
import uuid

from flask import Flask, make_response, render_template, request, jsonify
from flask_caching import Cache
from bankid import BankIDJSONClient
from bankid.certutils import create_bankid_test_server_cert_and_key

USE_TEST_SERVER = True

app = Flask(__name__)
cache = Cache(app, config={"CACHE_TYPE": "SimpleCache"})

# The client should be initialized in a better way, e.g. with Flask_BankID so that it is stored in the
# Flask app. For this demo it is sufficient to let it reside globally in this file.
if USE_TEST_SERVER:
    cert_paths = create_bankid_test_server_cert_and_key(str(pathlib.Path(__file__).parent))
    client = BankIDJSONClient(cert_paths, test_server=True)
else:
    # Set your own cert paths for you production certificate and key here.
    # Note that my recommendation is to get it to work with
    # test server certs first!
    cert_paths = ("certificate.pem", "key.pem")
    client = BankIDJSONClient(cert_paths, test_server=False)


# Frontend pages


@app.route("/")
def index():
    """Landing page, with form to fill in Personal Identity Number"""
    return render_template("index.html")


@app.route("/auth-complete")
def auth_complete():
    """When the authentication is either completed or failed, this is where the user ends up"""
    # Try to get the cookie set from the collect method,
    auth_cookie = request.cookies.get("QRDemo-Auth")
    if auth_cookie:
        # There was a cookie. Get the collect response stored in the cache.
        collect_response = cache.get(uuid.UUID(auth_cookie))
    else:
        # No cookie. Authentication failed.
        collect_response = {}
        age = None

    response = make_response(render_template("auth_complete.html", auth=collect_response))
    # Unsetting the cookie to make the app capable of being run again.
    response.set_cookie("QRDemo-Auth", "", expires=0)
    return response


# Backend API methods


@app.route("/send-initiate", methods=["POST"])
def initiate():
    """Initiate a BankID Authentication session and cache details needed for QR code generation"""
    # Note that empty personal number is allowed here! That means that the
    pn = request.form.get("personnumer")

    # From (https://www.bankid.com/assets/bankid/rp/bankid-relying-party-guidelines-v3.6.pdf):
    # Note: If personal number is included in the call to the service, RP must
    # consider setting the requirement tokenStartRequired to true. By this, the
    # system enforces that no other device than the one started using the QR code
    # or autoStartToken is used.

    # Make Auth call to BankID.
    resp = client.authenticate(
        end_user_ip=request.remote_addr,  # Get the IP of the device making the request.
        personal_number=pn,
        requirement={"tokenStartRequired": True if pn else False},  # Set to True if PN is provided. Recommended.
    )
    # Record when this response was received. This is needed for generating sequential, animated QR codes.
    resp["start_t"] = time.time()
    # Store these details for later use in some way. Here I use a very simple memory cache; not recommended for
    # multi-instance apps. Using orderRef as key since it is unique and can be sent in a GET URL without problem.
    cache.set(resp.get("orderRef"), resp, timeout=5 * 60)
    # Generate the first QR code to display to user.
    qr_content_0 = generate_qr_code_content(resp["qrStartToken"], resp["start_t"], resp["qrStartSecret"])
    return render_template(
        "qr.html",
        order_ref=resp["orderRef"],
        auto_start_token=resp["autoStartToken"],
        qr_content=qr_content_0,
    )


@app.route("/get-qr-code/<order_ref>")
def get_qr_code(order_ref: str):
    """Get the current QR code content to generate QR code from"""
    x = cache.get(order_ref)
    if x is None:
        qr_content = ""
    else:
        qr_content = generate_qr_code_content(x["qrStartToken"], x["start_t"], x["qrStartSecret"])
    response = make_response(qr_content, 200)
    response.mimetype = "text/plain"
    return response


@app.route("/collect/<order_ref>")
def collect(order_ref: str):
    """Make collect calls to the BankID servers"""
    collect_response = client.collect(order_ref)
    if collect_response.get("status") == "complete":
        # Create or Login the newly authenticated user, give it a session token or something similar.
        # Here I will use an ugly hack and just stick a generated UUID in a cookie so the frontend can tell
        # the next page that it is successfully signed in. The collect response is then stored in the cache using
        # the same UUID so that it can be recovered later.
        # Note that this is NOT production quality code, merely for proving a point.
        session_id = uuid.uuid4()
        cache.set(session_id, collect_response)
        response = make_response(collect_response, 200)
        response.mimetype = "application/json"
        response.set_cookie("QRDemo-Auth", str(session_id))
        return response
    else:
        return jsonify(collect_response)


# Helper methods


def generate_qr_code_content(qr_start_token: str, start_t: float, qr_start_secret: str):
    """Given QR start token, time.time() when initiated authentication call was made and the
    QR start secret, calculate the current QR code content to display.
    """
    elapsed_seconds_since_call = int(floor(time.time() - start_t))
    qr_auth_code = hmac.new(
        qr_start_secret.encode(),
        msg=str(elapsed_seconds_since_call).encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()
    return f"bankid.{qr_start_token}.{elapsed_seconds_since_call}.{qr_auth_code}"
