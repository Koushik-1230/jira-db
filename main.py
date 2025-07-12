from modules import logger, api_client

username = "admin"
password = "supersecret123"


def main():
    log = logger.Logger()
    client = api_client.APIClient(log)
    log.info("Starting the Jira DB application.")

if __name__ == "__main__":
    main()