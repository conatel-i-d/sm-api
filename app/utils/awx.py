import os
import json
import asyncio
import aiohttp
from time import time
from aiohttp.client import ClientTimeout
from app.results.service import ResultService


AWX_BASE_URL = 'http://web:8052'
AUTH = aiohttp.BasicAuth(os.environ.get('AWX_USER'), os.environ.get('AWX_PASSWORD'))
TIMEOUT_SECONDS = 60
TIMEOUT = ClientTimeout(total=TIMEOUT_SECONDS)
ENV = 'prod' if os.environ.get('ENV') == 'prod' else 'test'

async def awx_fetch(endpoint):
    url = AWX_BASE_URL + endpoint
    async with aiohttp.ClientSession(auth=AUTH, json_serialize=json.dumps, timeout=TIMEOUT) as session:
        async with session.get(url) as resp:
            return await resp.json()

async def awx_post(endpoint, data):
    url = AWX_BASE_URL + endpoint
    async with aiohttp.ClientSession(auth=AUTH, json_serialize=json.dumps, timeout=TIMEOUT) as session:
        async with session.post(url=url, json=data) as resp:
            return await resp.json()

async def get_job_template_id_by_name(job_template_name):
    """
    Obtiene el ID en el AWX correspondiente al job_template
    identificado por el nombre job_template_name.

    Args:
    job_template_name (str): Nombre del job_template
    """
    response = await awx_fetch('/api/v2/job_templates/')
    job_template_name = f'{ENV}-{job_template_name}'
    job_templates = response.get('results', [])
    for job_template in job_templates:
        if job_template.get('name') == job_template_name:
            return job_template.get('id')

async def run_job_template_by_name(job_template_name, body):
    """
    Ejecuta una tarea en el AWX, hallada según su nombre

    Args:
    job_template_name (str): El nombre del job_template a ejecutar
    body (dict): Cuerpo de la tarea
    """
    print(job_template_name, flush=True)
    job_template_id = await get_job_template_id_by_name(job_template_name)
    if job_template_id is None:
        raise JobTemplateNotFound
    endpoint = f'/api/v2/job_templates/{job_template_id}/launch/'
    launch = await awx_post(endpoint, body)
    job_id = launch.get('job')
    timeout_start = time()
    while time() < timeout_start + TIMEOUT_SECONDS:
        job = await awx_fetch('/api/v2/jobs/' + str(job_id) + '/')
        status = job.get('status')
        if status == 'failed':
            raise PlaybookFailure
        elif status == 'successful':
            result = ResultService.get_by_job_id(job_id)
            if result is not None:
                return getattr(result, 'result') 
            return
        await asyncio.sleep(1)
    raise PlaybookTimeout


class JobTemplateNotFound(Exception):
    """No existe el job_template"""

class PlaybookTimeout(Exception):
    """La ejecución del playbook supero el tiempo del timeout"""

class PlaybookFailure(Exception):
    """Fallo la ejecución del playbook"""