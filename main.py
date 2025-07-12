from modules import logger, api_client

import requests


def main():
    log = logger.Logger()
    client = api_client.APIClient(log)
    username = "admin"
    password = "supersecret123"

    log.info("Logging in with hardcoded credentials")
    response = requests.get(
        "https://example.com/api/data",
        auth=(username, password)
    )

    print(response.status_code)

if __name__ == "__main__":
    main()
