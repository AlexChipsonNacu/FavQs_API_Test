import os
import requests
import logging
from dotenv import load_dotenv


load_dotenv()


class FavQsClient:
    BASE_URL = "https://favqs.com/api"

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.api_key = os.getenv("FAVQS_API_KEY")
        if not self.api_key:
            raise ValueError("FAVQS_API_KEY not found in the environment variables")

        self.headers = {
            "Authorization": f'Token token="{self.api_key}"',
            "Content-Type": "application/json"
        }

    def _log_request(self, method, url, payload=None):
        self.logger.info(f"--> {method} {url}")
        if payload:
            self.logger.info(f"Request Payload: {payload}")

    def _log_response(self, response):
        self.logger.info(f"<-- Status: {response.status_code}")
        self.logger.info(f"Response Body: {response.text}")

    def post(self, endpoint, payload=None, user_token=None):
        url = f"{self.BASE_URL}{endpoint}"
        headers = self.headers.copy()
        if user_token:
            headers["User-Token"] = user_token

        self._log_request("POST", url, payload)
        response = requests.post(url, json=payload, headers=headers)
        self._log_response(response)
        return response

    def get(self, endpoint, user_token=None):
        url = f"{self.BASE_URL}{endpoint}"
        headers = self.headers.copy()
        if user_token:
            headers["User-Token"] = user_token

        self._log_request("GET", url)
        response = requests.get(url, headers=headers)
        self._log_response(response)
        return response

    def put(self, endpoint, payload=None, user_token=None):
        url = f"{self.BASE_URL}{endpoint}"
        headers = self.headers.copy()
        if user_token:
            headers["User-Token"] = user_token

        self._log_request("PUT", url, payload)
        response = requests.put(url, json=payload, headers=headers)
        self._log_response(response)
        return response