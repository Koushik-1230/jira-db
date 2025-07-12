import requests

from modules import api_client, logger

username = "admin"
password = "supersecret123"


def main():
    log = logger.Logger()
    client = api_client.APIClient(log)
    username = "admin"
    password = "supersecret123"
    log.info(f"{username} is logging in with hardcoded credentials {password}")

    log.info("Logging in with hardcoded credentials")
    response = requests.get("https://example.com/api/data", auth=(username, password))

    print(response.status_code)


if __name__ == "__main__":
    main()
