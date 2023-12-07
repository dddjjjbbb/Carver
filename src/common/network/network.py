import asyncio
import random
from typing import Union

import aiohttp
from aiohttp.client_exceptions import ClientConnectionError
import random
from fake_useragent import UserAgent
import random


import requests
from requests import Response
import time
from fake_headers import Headers

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


# def get(urls: [str]) -> [bytes]:
#     return asyncio.run(_get_response(urls))
#
#
# async def _get_response(urls: [str]) -> [bytes]:
#     tasks = []
#     for url in urls:
#         tasks.append(asyncio.ensure_future(_get_request(url)))
#
#     return await asyncio.gather(*tasks)
#
#
# async def _get_request(url) -> Union[bytes, None]:
#     try:
#         await asyncio.sleep(random.uniform(1, 5))
#         async with aiohttp.ClientSession() as session:
#             # Spoof headers to prevent blocking
#             ua = UserAgent()
#
#             headers = {
#                 "User-Agent": ua.random
#             }
#             async with session.get(url, headers=headers) as resp:
#                 return await resp.read()
#     except ClientConnectionError as e:
#         print(e)
#         return None