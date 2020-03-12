import os
import json
import aiohttp
from aiohttp.client import ClientTimeout


PRIME_API_URL = 'http://primeapi'
AUTH = aiohttp.BasicAuth(os.getenv('CISCO_PRIME_USER') + ":" + os.getenv('CISCO_PRIME_PASSWORD'))
TIMEOUT_SECONDS = 60
TIMEOUT = ClientTimeout(total=TIMEOUT_SECONDS)

async def prime_fetch(endpoint):
    url = PRIME_API_URL + endpoint
    async with aiohttp.ClientSession(auth=AUTH, json_serialize=json.dumps, timeout=TIMEOUT) as session:
        async with session.get(url) as resp:
            return await resp.json()