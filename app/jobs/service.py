import asyncio
import os
import sys
from time import time

from app import db
from app.errors import JobTemplateNotFound, PlaybookTimeout, PlaybookFailure, ConnectToAwxFailure, PlaybookCancelFailure
from app.utils.awx import awx_fetch, awx_post
from typing import List
from .model import Job


ENV = 'prod' if os.environ.get('ENV') == 'prod' else 'dev'
TIMEOUT_SECONDS = 120


class JobService:
    @staticmethod
    def get_all() -> List[Job]:
        return Job.query.all()

    @staticmethod
    def get_by_id(id: int) -> Job:
        result =  Job.query.get(id)
        return result

    @staticmethod
    def get_by_job_id(id: int) -> Job:
        result =  Job.query.filter(Job.job_id == id).first()
        return result
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
        if model is None:
            return []
        
        db.session.delete(model)
        db.session.commit()
        return [id]
    
    @staticmethod
    def delete_by_job_id(job_id: int) -> List[int]:
        model = Job.query.filter(Job.job_id == job_id).first()
        if model is None:
            return []
        db.session.delete(model)
        db.session.commit()
        return [job_id]

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
    @classmethod
    async def run_job_template_by_name(cls, job_template_name, body):
        """
        Ejecuta una tarea en el AWX, hallada según su nombre

        Args:
        job_template_name (str): El nombre del job_template a ejecutar
        body (dict): Cuerpo de la tarea
        """
        print(job_template_name, flush=True)
        job_template_id = await cls.get_job_template_id_by_name(job_template_name)
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
                result = cls.get_by_job_id(job_id)
                if result is not None:
                    cls.delete_by_job_id(job_id)
                    return getattr(result, 'result')
                return
            await asyncio.sleep(1)
        raise PlaybookTimeout

    @classmethod
    async def get_jobs_from_awx(cls):
        """
        Solicita a AWX y luego devuelve la lista de Jobs con sus respectivos estados

        Args:
        """
        return await awx_fetch("/api/v2/jobs?order_by=-created&page_size=100")

    @classmethod
    async def cancel_jobs_by_template_name_and_host_name(cls, job_template_name, limit_host_name):
        try:
            all_jobs = list((await JobService.get_jobs_from_awx())["results"])
        except:
            raise ConnectToAwxFailure
        jobs_for_cancel = filter(
            lambda x:
                x["summary_fields"]["job_template"]["name"] == job_template_name and
                x["limit"] == limit_host_name and
                x["status"] in ["running","pending","waiting"],
                all_jobs )
        for job in jobs_for_cancel:
            try:
                await awx_post(f'/api/v2/jobs/{job["id"]}/cancel/', None)
            except:
                raise PlaybookCancelFailure
        return True
