from modules import logger, api_client

def main():
    log = logger.Logger()
    client = api_client.APIClient(log)
    log.info("Starting the Jira DB application.")

if __name__ == "__main__":
    main()