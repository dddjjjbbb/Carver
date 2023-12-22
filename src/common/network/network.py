import time

import requests
from fake_headers import Headers
from requests import Response


def get(url) -> Response:
    """
    Send a request to the given URL and return the response.
    """

    headers = Headers(os="mac", headers=True).generate()

    try:
        response = requests.get(url, headers=headers)
        return response
    except ConnectionError:
        print("Connection error occurred. Retrying...")
        time.sleep(1)  # Add a short delay before retrying
        response = requests.get(url, headers=headers)
        return response
