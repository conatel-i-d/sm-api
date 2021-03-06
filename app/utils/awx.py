import os
import json
import aiohttp
from aiohttp.client import ClientTimeout


AWX_BASE_URL = 'http://web:8052'
AUTH = aiohttp.BasicAuth(os.environ.get('AWX_USER'), os.environ.get('AWX_PASSWORD'))
TIMEOUT_SECONDS = 60
TIMEOUT = ClientTimeout(total=TIMEOUT_SECONDS)

async def awx_fetch(endpoint):
    url = AWX_BASE_URL + endpoint
    async with aiohttp.ClientSession(auth=AUTH, json_serialize=json.dumps, timeout=TIMEOUT) as session:
        async with session.get(url) as resp:
            return await resp.json()

async def awx_post(endpoint, data):
    url = AWX_BASE_URL + endpoint
    if data != None:
        async with aiohttp.ClientSession(auth=AUTH, json_serialize=json.dumps, timeout=TIMEOUT) as session:
            async with session.post(url=url, json=data) as resp:
                return await resp.json()
    else:
        async with aiohttp.ClientSession(auth=AUTH, timeout=TIMEOUT) as session:
            async with session.post(url=url) as resp:
                return await resp.text()


