from app import db
from typing import List
from .model import Switch
from app.utils.b64 import encode
from app.errors import ApiException
import os
import json
import sys
from app.utils.prime import prime_fetch
import copy
import pathlib

import asyncio
from app.jobs.service import JobService

class SwitchService:
    @staticmethod
    async def get_all() -> List[Switch]:
        switches_from_prime = []
        try:
            db_switches = Switch.query.all()
            sw_names_in_db =  list(map(lambda x: x.name, db_switches))
            sw_ids_in_db = list(map(lambda x: x.id, db_switches))
            prime_data = await prime_fetch('/webacs/api/v4/data/Devices.json?.full=true&.maxResults=300&.firstResult=0')
            switches = prime_data['queryResponse']['entity']
            for switch in switches:
                switch_data = switch["devicesDTO"]
                if not (switch_data["deviceName"] in sw_names_in_db) and not (switch_data["deviceId"] in sw_ids_in_db):
                    SwitchService.create({
                        "id": int(switch_data["deviceId"]),
                        "name": switch_data["deviceName"],
                        "description": "software_type: {0}, software_version: {1}".format(switch_data.get("softwareType","unknown"),switch_data.get("softwareVersion","unknown")),
                        "model": switch_data["deviceType"], 
                        "ip": switch_data["ipAddress"],
                        "ansible_user": encode(os.getenv("PRIME_SWITCHES_SSH_USER")),
                        "ansible_ssh_pass": encode(os.getenv("PRIME_SWITCHES_SSH_PASS")),
                        "is_visible": True
                        })
                else:
                    db.session.query(Switch).filter(
                        Switch.name == switch_data["name"] or Switch.id == int(switch_data["deviceId"])).update(
                        {
                            "id": int(switch_data["deviceId"]),
                            "name": switch_data["deviceName"],
                            "description": "software_type: {0}, software_version: {1}".format(switch_data.get("softwareType","unknown"),switch_data.get("softwareVersion","unknown")),
                            "model": switch_data["deviceType"], 
                            "ip": switch_data["ipAddress"],
                            "ansible_user": encode(os.getenv("PRIME_SWITCHES_SSH_USER")),
                            "ansible_ssh_pass": encode(os.getenv("PRIME_SWITCHES_SSH_PASS"))
                        })
        except Exception as err:
            print("Can't connect with prime to list switches, error: ", err, flush=True)
            raise ApiException("Can't connect with prime to list switches", 500, code="CiscoPrimeError")
        return db.session.query(Switch).all()
    
    @staticmethod
    async def get_by_id(id: int) -> Switch:
        sws = await SwitchService.get_all()
        if len(sws) > 0:
            switch = list(filter(lambda x: x.id == int(id), sws))
            if len(switch) > 0:
                return switch[0]
        raise SwitchNotFound

    @staticmethod
    def update(id: int, body) -> Switch:
        model = Switch.query.get(id)
        if model is None:
            raise SwitchNotFound
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

    @staticmethod
    async def get_macs(switch_id, nic_name):
        switch = SwitchService.get_by_id(switch_id)
        if switch == None:
            raise SwitchNotFound
        extra_vars = dict(interface_name=nic_name)
        body = dict(limit=switch.name, extra_vars=extra_vars)
        return await JobService.run_job_template_by_name('get-mac-address-table', body)

class SwitchNotFound(Exception):
    """No existe el switch"""