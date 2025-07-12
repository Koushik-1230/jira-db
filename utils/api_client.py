"""
API Client module for handling HTTP requests with retry logic and concurrency control.
"""
import base64
from datetime import datetime
import os
import time
from dotenv import load_dotenv
load_dotenv()

import requests



class APIClient:
    """
    A client for making HTTP requests.
    """
    def __init__(self, logger):
        """
        Initialize the API client.
        
        Args:
            logger (Logger): Logger instance for logging API requests and responses.
        """
        self.logger = logger
        self.jira_url = os.getenv("JIRA_BASE_URL")
        self.jira_email = os.getenv("JIRA_EMAIL")
        self.jira_token = os.getenv("JIRA_API_TOKEN")
        self.default_timeout = 10
        self.jira_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {base64.b64encode(f"{self.jira_email}:{self.jira_token}".encode()).decode()}",
            }
        if not self.jira_url or not self.jira_email or not self.jira_token:
            raise ValueError("JIRA_URL, JIRA_EMAIL, and JIRA_TOKEN environment variables must be set.")
        self.logger.info(f"API Client initialized with JIRA URL: {self.jira_url}")
    
    def get_request(self, *args ,**kwargs):
        """
        Make a GET request with retry logic.
        
        Args:
            *args: Positional arguments for the request.
            **kwargs: Keyword arguments for the request.
        
        Returns:
            Response object from the requests library.
        """
        url = None
        headers = None
        request_to = list(args)[0]
        endpoint = list(args)[1]
        params = kwargs.get("params", {})
        self.logger.info(f"GET request to {request_to} at {endpoint} with params: {params}")
        if request_to.lower() == "jira":
            url = f"{self.jira_url}{endpoint}"
            headers = self.jira_headers
        else:
            raise ValueError("Unsupported request_to value. Only 'jira' is supported.")
        self.logger.info(f"Making GET request to {url} with headers: {headers} and params: {params}")
        try:
            response = requests.get(url, headers=headers, params=params, timeout=self.default_timeout)
            response.raise_for_status()
            self.logger.info(f"GET request to {url} successfully returned status code {response.status_code}.")
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"GET request to {url} failed: {e}")
            return None
        except Exception as e:
            self.logger.error(f"An unexpected error occurred during GET request: {e}")
            return None
        


        
        

        

    
