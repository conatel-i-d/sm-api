import os
import json
import aiohttp
from aiohttp.client import ClientTimeout
import sys

PRIME_API_URL = os.getenv('CISCO_PRIME_BASE_USER')
AUTH = aiohttp.BasicAuth(os.getenv('CISCO_PRIME_USER'), os.getenv('CISCO_PRIME_PASSWORD'))
TIMEOUT_SECONDS = 60
TIMEOUT = ClientTimeout(total=TIMEOUT_SECONDS)

async def prime_fetch(endpoint):
    print("=====================================================", file=sys.stdout)
    url = PRIME_API_URL + endpoint
    print("prime url: " + url, file=sys.stderr)
    print("prime user: " + os.getenv('CISCO_PRIME_USER'), file=sys.stderr)
    print("prime pass: " + os.getenv('CISCO_PRIME_PASSWORD'), file=sys.stderr)
    async with aiohttp.ClientSession(auth=AUTH, json_serialize=json.dumps, timeout=TIMEOUT, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get(url) as resp:
            return await resp.json()
