# QR Authentication Example

Making a simple authentication via QR code solution using Flask, Flask-Caching and PyBankID.

## Running the application

1. Navigate your terminal to the same folder that this README resides in.
2. Create a virtualenv: `python -m venv .venv`
3. Activate it.
4. Install requirements: `pip install -r requirements.txt`
5. Run flask app:
   1. From Bash:
      ```bash
      $ export FLASK_APP=qrdemo.app:app
      $ flask run -h 0.0.0.0
      ```
   2. From Powershell:
      ```powershell
      > $env:FLASK_APP = "qrdemo.app:app"
      > flask run -h 0.0.0.0
      ```

The app can now be accessed from the running computer on `http://127.0.0.1:5000`, `http://localhost:5000` or from an 
external device on the same network on `http://<ip for the running computer>:5000`.


## Basic workflow

These are the steps that the application takes:

1. Ask the user for Swedish Personal Identity Number (PN).
2. Upon POSTing that PN to the backend, initiate a BankID `authenticate` session. This generates tokens that
   one can create QR codes from using the `generate_qr_code_content` method.
3. Continuously update the QR code according to the description in the BankID Relying Party Guidelines
   Version: 3.6 (see below, Chapter 4). The new QR code content to display MUST be fetched from the backend since
   the `qrStartSecret` must never be shown to the user for the authentication to be trustworthy.
4. Also make `collect` calls to the BankID servers continuously and monitor if signing is complete or failed.
5. Redirect when complete or failed.
 

## Missing components

There are a few shortcuts taken here:

- There is no error handling of `status: failed` results when collecting the authentication response.
- There is no `Recommended User Messages (RFA)` handling. It merely displays the `status` and `hintCode` from the collect response.
- The Cache is a memory cache on this single instance web app.

## References

[BankID Relying Party Guidelines
Version: 3.6](https://www.bankid.com/assets/bankid/rp/bankid-relying-party-guidelines-v3.6.pdf)
