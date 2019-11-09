import asyncio
import aiohttp
async def awx_fetch(endpoint):
    url = 'http://web:8052/api/v2/hosts/'
    auth = aiohttp.BasicAuth("awx", "awxpassword")
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(url) as resp:
            return await resp.json()