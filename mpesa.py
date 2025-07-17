import os
import base64
import requests

from requests.auth import HTTPBasicAuth
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()


class Mpesa:
    consumer_key = None
    consumer_secret = None
    business_short_code = "174379"
    timestamp = None

    def __init__(self):
        self.consumer_key = os.environ.get("CONSUMER_KEY")
        self.consumer_secret = os.environ.get("CONSUMER_SECRET")
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    def get_access_token(self):
        """
        -> Generate access tokens that will be used in subsequent request
        to mpesa
        -> The token has a timespan of 1hr
        """

        # 1. Retrieve token from our storage and if it still active, we use it
        # else we get a new one from saf
        # stored_data = MpesaAccessToken

        res = requests.get(
            "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
            auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
        )

        data = res.json()
        # store the token somewhere

        return data["access_token"]

    def generate_password(self):
        """
        -> Generate password by combining the shortcode, passkey & current timestamp
        """
        password_str = (
            self.business_short_code + os.environ.get("SAF_PASS_KEY") + self.timestamp
        )

        return base64.b64encode(password_str.encode()).decode("utf-8")

    def make_stk_push(self, data):
        amount = data["amount"]
        phone = data["phone"]
        desc = data["description"]

        body = {
            "BusinessShortCode": self.business_short_code,
            "Password": self.generate_password(),
            "Timestamp": self.timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": self.business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://b68a567c1b34.ngrok-free.app/payments/callback",
            "AccountReference": "Notted",
            "TransactionDesc": desc,
        }

        token = self.get_access_token()

        response = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
            json=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )

        response_data = response.json()
        return response_data

    def check_transaction(self, checkout_request_id):
        """
        -> Checks whether an skt push was successful or not
        """
        data = {
            "BusinessShortCode": self.business_short_code,
            "Password": self.generate_password(),
            "Timestamp": self.timestamp,
            "CheckoutRequestID": checkout_request_id,
        }

        token = self.get_access_token()

        response = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query",
            json=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )

        return response.json()
