"""
API Client module for handling HTTP requests with retry logic and concurrency control.
"""
from threading import Lock

import requests
from requests.adapters import HTTPAdapter, Retry
from packaging import version


class APIClient:
    """
    A robust HTTP client with retry logic, concurrency control, and error handling.
    
    This class provides a thread-safe interface for making HTTP requests with
    automatic retry capabilities and proper connection pooling.
    """
    
    def __init__(self, max_retries=5, backoff_factor=1, concurrency=10):
        """
        Initialize the API client.
        
        Args:
            max_retries (int): Maximum number of retry attempts for failed requests
            backoff_factor (float): Multiplier for retry delays
            concurrency (int): Maximum number of concurrent connections
        """
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.concurrency = concurrency
        self.session = self._create_session()
        self.lock = Lock()

    def _create_session(self):
        """
        Create and configure a requests session with retry strategy.
        
        Returns:
            requests.Session: Configured session object
        """
        # Define the HTTP methods to retry
        retry_methods = ["GET", "POST", "PUT", "DELETE"]

        # Check requests version to use appropriate parameter name
        requests_version = version.parse(requests.__version__)
        retry_params = {
            'total': self.max_retries,
            'backoff_factor': self.backoff_factor,
            'status_forcelist': [429, 500, 502, 503, 504],
        }

        # Use appropriate parameter name based on version
        if requests_version >= version.parse('2.26.0'):
            retry_params['allowed_methods'] = retry_methods
        else:
            retry_params['method_whitelist'] = retry_methods

        retry_strategy = Retry(**retry_params)
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_maxsize=self.concurrency)
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def get_request(self, url, headers, params=None):
        """
        Make a GET request to the specified URL.
        
        Args:
            url (str): The URL to send the request to
            headers (dict): HTTP headers to include in the request
            params (dict, optional): Query parameters to include
            
        Returns:
            tuple: (response_data, status_code, status_message)
        """
        try:
            with self.lock:
                response = self.session.get(url, headers=headers, params=params)
            status_code = response.status_code
            if status_code in [200, 201, 204]:
                return response.json() if response.text else {}, status_code, "successful"
            return response.json() if response.text else {}, status_code, "failed"
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500, "failed"

    def post_request(self, url, headers, data=None, files=None):
        """
        Make a POST request to the specified URL.
        
        Args:
            url (str): The URL to send the request to
            headers (dict): HTTP headers to include in the request
            data (dict, optional): JSON data to include in the request body
            files (dict, optional): Files to upload
            
        Returns:
            tuple: (response_data, status_code, status_message)
        """
        try:
            with self.lock:
                if files:
                    response = self.session.post(url, headers=headers, files=files)
                else:
                    response = self.session.post(url, json=data, headers=headers)
            status_code = response.status_code
            if status_code in [200, 201, 204]:
                return response.json() if response.text else {}, status_code, "successful"
            return response.json() if response.text else {}, status_code, "failed"
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500, "failed"

    def put_request(self, url, headers, data=None, files=None):
        """
        Make a PUT request to the specified URL.
        
        Args:
            url (str): The URL to send the request to
            headers (dict): HTTP headers to include in the request
            data (dict, optional): JSON data to include in the request body
            files (dict, optional): Files to upload
            
        Returns:
            tuple: (response_data, status_code, status_message)
        """
        try:
            with self.lock:
                if files:
                    response = self.session.put(url, headers=headers, files=files)
                else:
                    response = self.session.put(url, json=data, headers=headers)
            status_code = response.status_code
            if status_code in [200, 201, 204]:
                return response.json() if response.text else {}, status_code, "successful"
            return response.json() if response.text else {}, status_code, "failed"
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500, "failed"

    def delete_request(self, url, headers):
        """
        Make a DELETE request to the specified URL.
        
        Args:
            url (str): The URL to send the request to
            headers (dict): HTTP headers to include in the request
            
        Returns:
            tuple: (response_data, status_code, status_message)
        """
        try:
            with self.lock:
                response = self.session.delete(url, headers=headers)
            status_code = response.status_code
            if status_code in [200, 201, 204]:
                return response.json() if response.text else {}, status_code, "successful"
            return response.json() if response.text else {}, status_code, "failed"
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500, "failed"

    def close(self):
        """
        Close the session and clean up resources.
        """
        self.session.close()