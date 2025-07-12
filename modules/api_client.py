"""This module defines the APIClient for interacting with the Jira REST API."""

import base64
import os
import time
import requests


class APIClient:
    """Handles requests to the Jira API using provided credentials."""

    def __init__(self, logger):
        """Initializes the APIClient with Jira credentials and sets up headers."""
        self.logger = logger
        self.jira_url = os.getenv("JIRA_BASE_URL")
        self.jira_email = os.getenv("JIRA_EMAIL")
        self.jira_token = os.getenv("JIRA_API_TOKEN")
        if not all([self.jira_url, self.jira_email, self.jira_token]):
            raise ValueError(
                "JIRA_URL, JIRA_EMAIL, and JIRA_TOKEN must be set in environment variables."
            )
        credentials = f"{self.jira_email}:{self.jira_token}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.jira_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_credentials}",
        }
        self.logger.info("APIClient initialized with JIRA credentials.")

    def send_request(self, request_to, endpoint, method,
                     data=None):
        """
        Sends an HTTP request to the specified API.

        Args:
            request_to (str): Target system (e.g., "jira").
            endpoint (str): API endpoint path.
            method (str): HTTP method ("GET", "POST", "PUT", "DELETE").
            data (dict, optional): JSON payload.
            files (dict, optional): Files to upload.
            params (dict, optional): URL parameters.

        Returns:
            tuple: (response JSON or None, message string)
        """
        time.sleep(1)  # To avoid rate limiting
        url = None
        headers = None

        if request_to == "jira":
            url = f"{self.jira_url}{endpoint}"
            headers = self.jira_headers
        else:
            self.logger.error(f"Unknown request target: {request_to}")
            return None, "Unknown request target"

        try:
            response = None
            method = method.lower()
            if method == "get":
                response = requests.get(url, headers=headers, timeout=10)
            elif method == "post":
                response = requests.post(url, headers=headers, json=data, timeout=10)
            elif method == "put":
                response = requests.put(url, headers=headers, json=data, timeout=10)
            elif method == "delete":
                response = requests.delete(url, headers=headers, timeout=10)
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
