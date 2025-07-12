import base64
import time
import os

import requests


class APIClient:
    def __init__(self, logger):
        self.logger = logger
        self.jira_url = os.getenv("JIRA_BASE_URL")
        self.jira_email = os.getenv("JIRA_EMAIL")
        self.jira_token = os.getenv("JIRA_API_TOKEN")
        if not all([self.jira_url, self.jira_email, self.jira_token]):
            raise ValueError(
                "JIRA_URL, JIRA_EMAIL, and JIRA_TOKEN must be set in environment variables."
            )
        self.jira_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {base64.b64encode(f'{self.jira_email}:{self.jira_token}'.encode()).decode()}",
        }
        self.logger.info("APIClient initialized with JIRA credentials.")

    def send_request(
        self, request_to, endpoint, method, data=None, files=None, params=None
    ):
        time.sleep(1)  # To Avoid Rate limiting
        url = None
        headers = None
        if request_to == "jira":
            url = f"{self.jira_url}{endpoint}"
            headers = self.jira_headers
        else:
            self.logger.error(f"Unknown request target: {request_to}")
            return None, "Unknown request target"
        try:
            if method.lower() == "get":
                response = requests.get(url, headers=headers, params=params)
            elif method.lower() == "post":
                response = requests.post(url, headers=headers, json=data, files=files)
            elif method.lower() == "put":
                response = requests.put(url, headers=headers, json=data)
            elif method.lower() == "delete":
                response = requests.delete(url, headers=headers)
            else:
                self.logger.error(f"Unsupported HTTP method: {method}")
                return None, "Unsupported HTTP method"

            response.raise_for_status()
            self.logger.info(
                f"Request to {url} successful with status code {response.status_code}."
            )
            return response.json(), "Success"
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request to {url} failed: {e}")
            return None, str(e)
