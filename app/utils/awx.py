import asyncio
import aiohttp
from aiohttp.client import ClientTimeout
import os
import json
awx_base_url = 'http://web:8052'
auth = aiohttp.BasicAuth(os.environ.get('AWX_USER'), os.environ.get('AWX_PASSWORD'))
timeout = ClientTimeout(total=60)
async def awx_fetch(endpoint):
    url = awx_base_url + endpoint

    async with aiohttp.ClientSession(auth=auth, json_serialize=json.dumps, timeout=timeout) as session:
        async with session.get(url) as resp:
            return await resp.json()

async def awx_post(endpoint, data):
    url = awx_base_url + endpoint
    async with aiohttp.ClientSession(auth=auth, json_serialize=json.dumps, timeout=timeout) as session:
        async with session.post(url=url, json=data) as resp:
            return await resp.json()