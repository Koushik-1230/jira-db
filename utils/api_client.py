"""
API Client module for handling HTTP requests with retry logic and concurrency control.
"""
import base64
from datetime import datetime
import os
import time

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
        self.jira_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {base64.b64encode(f"{self.jira_email}:{self.jira_token}".encode()).decode()}",
            }
        if not self.jira_url or not self.jira_email or not self.jira_token:
            raise ValueError("JIRA_URL, JIRA_EMAIL, and JIRA_TOKEN environment variables must be set.")
        self.logger.info(f"API Client initialized with JIRA URL: {self.jira_url}")
    
    def make_request(self, request_to, endpoint):
        """
        Make an HTTP request with retry logic.
        
        Args:
            method (str): HTTP method (GET, POST, etc.).
            endpoint (str): API endpoint to call.
            *args: Positional arguments for the request.
            **kwargs: Keyword arguments for the request.
        
        Returns:
            Response object from the requests library.
        """
        self.logger.info("Making request to %s with args: %s, kwargs: %s", request_to, endpoint)

    
    def get_request(self, *args ,**kwargs):
        """
        Make a GET request with retry logic.
        
        Args:
            request_to (str): The base URL for the request.
            endpoint (str): The specific endpoint to call.
            *args: Positional arguments for the request.
            **kwargs: Keyword arguments for the request.
        
        Returns:
            Response object from the requests library.
        """
        self.logger.info(f"{args} {kwargs}")
        
        

        

    
