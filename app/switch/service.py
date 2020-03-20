from app import db
from typing import List
from .model import Switch
import base64
import os
import json
import sys

from app.utils.prime import prime_fetch

class SwitchService:
    @staticmethod
    async def get_all() -> List[Switch]:
        switches_from_prime = []
        try:
            prime_data = await prime_fetch('/webacs/api/v4/data/Devices.json?.full=true')
            switches = prime_data['queryResponse']['entity']
            for switch in switches:
                switch_data = switch["devicesDTO"]
                switches_from_prime.append(
                    Switch(
                        id=switch_data["deviceId"],
                        name=switch_data["deviceName"],
                        description="software_type: {0}, software_version: {1}".format(switch_data["softwareType"],switch_data["softwareVersion"]),
                        model=switch_data["deviceType"], 
                        ip=switch_data["ipAddress"]
                    )
                )
        except Exception as err:
            print("Can't connect with prime to list switches, error: ", err, file=sys.stderr)
        switches_from_db = Switch.query.all()
        return switches_from_db + switches_from_prime
    
    @staticmethod
    async def get_by_id(id: int) -> Switch:
        found_in_db = Switch.query.get(id)
        if found_in_db is None:
            prime_data = await prime_fetch('/webacs/api/v4/data/Devices.json?.full=true')
            switches = prime_data['queryResponse']['entity']
            swtich = filter(lambda x: x["devicesDTO"]["deviceId"] == id, switches)
            if len(swtich) > 0:
                return swtich[0]
            return None
        return found_in_db
    @staticmethod
    def update(id: int, body) -> Switch:
        model = SwitchService.get_by_id(id)
        if model is None:
            return None
        model.update(body)
        db.session.commit()
        return model

    @staticmethod
    def delete_by_id(id: int) -> List[int]:
        model = Switch.query.filter(Switch.id == id).first()
        if not model:
            return []
        db.session.delete(model)
        db.session.commit()
        return [id]

    @staticmethod
    def create(new_attrs) -> Switch:
        model = Switch(**new_attrs)

        db.session.add(model)
        db.session.commit()

        return model
