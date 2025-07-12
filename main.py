from modules import logger, api_client

import requests

username = "admin"
password = "supersecret123"


def main():
    log = logger.Logger()
    client = api_client.APIClient(log)

    log.info("Logging in with hardcoded credentials")
    response = requests.get("https://example.com/api/data", auth=(username, password))

    print(response.status_code)


if __name__ == "__main__":
    main()
