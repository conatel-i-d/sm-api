from app import db
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