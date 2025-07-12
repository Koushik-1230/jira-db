"""This module initializes and starts the Jira API client."""

from utils import api_client, logger

def main():
    """Main entry point to start the Jira API client."""
    log = logger.Logger()
    log.info("Starting Jira API client...")
    api_client.APIClient(log)

if __name__ == "__main__":
    main()
