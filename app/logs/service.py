from app import db
from typing import List
from .model import Log


class LogService:
    @staticmethod
    def get_all() -> List[Log]:
        return Log.query.all()

    @staticmethod
    def get_by_id(id: int) -> Log:
        return Log.query.get(id)

    @staticmethod
    def update(id: int, body) -> Log:
        model = LogService.get_by_id(id)
        if model is None:
            return None
        model.update(body)
        db.session.commit()
        return model

    @staticmethod
    def delete_by_id(id: int) -> List[int]:
        model = Log.query.filter(Log.id == id).first()
        if not model:
            return []
        db.session.delete(model)
        db.session.commit()
        return [id]

    @staticmethod
    def create(new_attrs) -> Log:
        model = Log(**new_attrs)

        db.session.add(model)
        db.session.commit()

        return model