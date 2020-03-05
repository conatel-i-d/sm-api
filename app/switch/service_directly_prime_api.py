from app import db
from typing import List
from .model import Switch
import base64
import os
import json

from app.utils.prime import prime_fetch

class SwitchService:
    @staticmethod
    async def get_all() -> List[Switch]:
        result = await prime_fetch('/webacs/api/v1/data/Devices.json')
        return result
    # @staticmethod
    # def get_by_id(id: int) -> Switch:
    #     return Switch.query.get(id)

    # @staticmethod
    # def update(id: int, body) -> Switch:
    #     model = SwitchService.get_by_id(id)
    #     if model is None:
    #         return None
    #     model.update(body)
    #     db.session.commit()
    #     return model

    # @staticmethod
    # def delete_by_id(id: int) -> List[int]:
    #     model = Switch.query.filter(Switch.id == id).first()
    #     if not model:
    #         return []
    #     db.session.delete(model)
    #     db.session.commit()
    #     return [id]

    # @staticmethod
    # def create(new_attrs) -> Switch:
    #     model = Switch(**new_attrs)

    #     db.session.add(model)
    #     db.session.commit()

    #     return model