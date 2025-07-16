import os
import requests
from requests.auth import HTTPBasicAuth

from dotenv import load_dotenv

load_dotenv()


class Mpesa:
    consumer_key = None
    consumer_secret = None

    def __init__(self):
        self.consumer_key = os.environ.get("CONSUMER_KEY")
        self.consumer_secret = os.environ.get("CONSUMER_SECRET")

    def get_access_token(self):
        """
        -> Generate access tokens that will be used in subsequent request
        to mpesa
        -> The token has a timespan of 1hr
        """
        res = requests.get(
            "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
            auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
        )

        data = res.json()
        return data["access_token"]
        # store the token somewhere
