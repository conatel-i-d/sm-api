from app import db
from typing import List
from .model import Switch
import base64
import os
import json
import sys
from app.utils.b64 import encode, decode
from app.utils.prime import prime_fetch
import copy
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
                        ip=switch_data["ipAddress"],
                        )
                )
        except Exception as err:
            print("Can't connect with prime to list switches, error: ", err, file=sys.stderr)
        sw_from_db = Switch.query.all()
        sw_from_db_dec_pass = []
        for sw in sw_from_db:
            sw.ansible_user = decode(sw.ansible_user)
            sw.ansible_ssh_pass = decode(sw.ansible_ssh_pass)
            sw_from_db_dec_pass.append(sw)
        return sw_from_db_dec_pass + switches_from_prime
    
    @staticmethod
    async def get_by_id(id: int) -> Switch:
        found_in_db = Switch.query.get(id)
        if found_in_db is None:
            prime_data = await prime_fetch('/webacs/api/v4/data/Devices.json?.full=true')
            switches = prime_data['queryResponse']['entity']
            swtich = list(filter(lambda x: x["devicesDTO"]["deviceId"] == id, switches))
            if len(swtich) > 0:
                switch_data = swtich[0]["devicesDTO"]
                return Switch(
                        id=switch_data["deviceId"],
                        name=switch_data["deviceName"],
                        description="software_type: {0}, software_version: {1}".format(switch_data["softwareType"],switch_data["softwareVersion"]),
                        model=switch_data["deviceType"], 
                        ip=switch_data["ipAddress"],
                        ansible_user=os.getenv("PRIME_SWITCHES_SSH_USER"),
                        ansible_ssh_pass=os.getenv("PRIME_SWITCHES_SSH_PASS")
                    )
            return None
        res = copy.copy(found_in_db)
        res.ansible_user: decode(found_in_db.ansible_user)
        res.ansible_ssh_pass: decode(found_in_db.ansible_ssh_pass)
        return res

    @staticmethod
    def update(id: int, body) -> Switch:
        model = Switch.query.get(id)
        if model is None:
            return None
        body["ansible_user"] = encode(body['ansible_user'])
        body["ansible_ssh_pass"] = encode(body['ansible_ssh_pass'])
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
        new_attrs = { **new_attrs, "ansible_user": encode(new_attrs['ansible_user'])} if new_attrs['ansible_user'] != None else new_attrs
        new_attrs = { **new_attrs, "ansible_ssh_pass": encode(new_attrs['ansible_ssh_pass'])} if new_attrs['ansible_ssh_pass'] != None else new_attrs
        model = Switch(**new_attrs)
        db.session.add(model)
        db.session.commit()

        return model
