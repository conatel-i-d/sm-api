import asyncio

from app import db
from app.errors import JobTemplateNotFound, PlaybookTimeout, PlaybookFailure
from typing import List
from .model import Job


class JobService:
    @staticmethod
    def get_all() -> List[Job]:
        return Job.query.all()

    @staticmethod
    def get_by_id(id: int) -> Job:
        return Job.query.get(id)
    
    @staticmethod
    def get(conditions) -> Job:
        return Job.query.filter_by(**conditions).first()

    @staticmethod
    def update(id: int, body) -> Job:
        model = JobService.get_by_id(id)
        if model is None:
            return None
        model.update(body)
        db.session.commit()
        return model

    @staticmethod
    def delete_by_id(id: int) -> List[int]:
        model = Job.query.filter(Job.id == id).first()
        if not model:
            return []
        db.session.delete(model)
        db.session.commit()
        return [id]

    @staticmethod
    def create(new_attrs) -> Job:
        model = Job(**new_attrs)

        db.session.add(model)
        db.session.commit()

        return model
    @staticmethod
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
    @staticmethod
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
