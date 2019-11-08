from flask import Flask
from utils.async_action import async_action
from utils.fetch import fetch
import asyncio
import aiohttp
import time
app = Flask(__name__)

@app.route('/')
@async_action
async def index():
    await asyncio.sleep(5)
    contador = 0
    async with aiohttp.ClientSession() as session:
        for i in range(10):
            print("before fetch")
            html = await fetch(session, 'https://api.telemetry.conatest.click/clients')
            print(html)
            contador += 1
    return 'Hello world whit total: ' + str(contador)

@app.route('/helloifr')
def hif():
    return 'Hello world whit total'

app.run()