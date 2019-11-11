from app import db
from typing import List
from .model import Result


class ResultService:
    @staticmethod
    def get_all() -> List[Result]:
        return Result.query.all()

    @staticmethod
    def get_by_id(id: int) -> Result:
        return Result.query.get(id)

    @staticmethod
    def update(id: int, body) -> Result:
        model = ResultService.get_by_id(id)
        if model is None:
            return None
        model.update(body)
        db.session.commit()
        return model

    @staticmethod
    def delete_by_id(id: int) -> List[int]:
        model = Result.query.filter(Result.id == id).first()
        if not model:
            return []
        db.session.delete(model)
        db.session.commit()
        return [id]

    @staticmethod
    def create(new_attrs) -> Result:
        model = Result(**new_attrs)

        db.session.add(model)
        db.session.commit()

        return model