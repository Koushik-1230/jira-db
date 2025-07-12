from .get_issues import get_issues
from ..utils.api_client import APIClient


class JiraDB:
    """
    Main class for interacting with Jira API.
    
    This class initializes
    the API client and provides methods to fetch issues from Jira.
    """
    def __init__(self, logger):
        """
        Initialize the JiraDB with a logger.
        
        Args:
            logger (Logger): Logger instance for logging.
        """
        self.logger = logger
        self.client = APIClient(logger)
        self.logger.info("JiraDB initialized with API client.")

    def fetch_issues(self):
        """
        Fetch issues from the specified Jira endpoint.
        
        Args:
            endpoint (str): The API endpoint to fetch issues from.
        
        Returns:
            list: A list of issues retrieved from the API.
        """
        return get_issues("jira", self.client)