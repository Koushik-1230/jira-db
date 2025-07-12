from modules import api_client, logger


def main():
    log = logger.Logger()
    log.info("Starting Jira API client...")
    api_client.APIClient(log)


if __name__ == "__main__":
    main()
