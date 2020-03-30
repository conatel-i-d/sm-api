from app import db
from typing import List
from .model import Switch
from app.utils.b64 import encode

import os
import json
import sys
from app.utils.prime import prime_fetch
import copy
import pathlib

class SwitchService:
    @staticmethod
    async def get_all() -> List[Switch]:
        switches_from_prime = []
        ids_sw_in_db =  map(lambda x: x[0], db.session.query(Switch.id).all())
        print(ids_sw_in_db,file=sys.stderr)
        try:
            # prime_data = await prime_fetch('/webacs/api/v4/data/Devices.json?.full=true')
            with open(os.path.join(pathlib.Path(__file__).parent.absolute(), 'prime_devices_full.json')) as json_file:
                prime_data = json.load(json_file)
            switches = prime_data['queryResponse']['entity']
            for switch in switches:
                switch_data = switch["devicesDTO"]
                if not (switch_data["deviceId"] in ids_sw_in_db):
                    SwitchService.create({
                        "id": switch_data["deviceId"],
                        "name": switch_data["deviceName"],
                        "description": "software_type: {0}, software_version: {1}".format(switch_data["softwareType"],switch_data["softwareVersion"]),
                        "model": switch_data["deviceType"], 
                        "ip": switch_data["ipAddress"],
                        "ansible_user": encode(os.getenv("PRIME_SWITCHES_SSH_USER")),
                        "ansible_ssh_pass": encode(os.getenv("PRIME_SWITCHES_SSH_PASS")),
                        "is_visible": True
                        })
                else:
                    SwitchService.update(switch_data["deviceId"],{
                        "name": switch_data["deviceName"],
                        "description": "software_type: {0}, software_version: {1}".format(switch_data["softwareType"],switch_data["softwareVersion"]),
                        "model": switch_data["deviceType"], 
                        "ip": switch_data["ipAddress"],
                        "ansible_user": encode(os.getenv("PRIME_SWITCHES_SSH_USER")),
                        "ansible_ssh_pass": encode(os.getenv("PRIME_SWITCHES_SSH_PASS"))
                        })
        except Exception as err:
            print("Can't connect with prime to list switches, error: ", err, file=sys.stderr)
        return db.session.query(Switch).all()
    
    @staticmethod
    async def get_by_id(id: int) -> Switch:
        sws = SwitchService.get_all()
        if len(sws) != 0 is None:
            switch = list(filter(lambda x: x.id == id, sws))
            if len(switch) > 0:
                return switch[0]
        return None

    @staticmethod
    def update(id: int, body) -> Switch:
        model = Switch.query.get(id)
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
