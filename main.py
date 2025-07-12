"""This module initializes and starts the Jira API client."""

from utils import api_client, logger
from modules import get_issues


class Main:
    """
    Main class to initialize and run the Jira API client.
    
    This class sets up the logger and starts the API client.
    """
    def __init__(self):
        """Initialize the Main class."""
        self.logger = logger.Logger()
        self.client = api_client.APIClient(self.logger)
        self.logger.info("Jira API client initialized successfully.")

    
    def test(self):
        """
        Test
        """
        self.logger.info("Testing the API Client")
        issues = get_issues.get_issues(self.client)
        if issues:
            self.logger.info(f"Fetched {len(issues)} issues from Jira.")
        else:
            self.logger.warning("No issues found in Jira.")
        



if __name__ == "__main__":
    main = Main()
    main.test()
    main.logger.info("Jira API client test completed successfully.")





