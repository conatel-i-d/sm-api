from app import db
from typing import List

from app.utils.b64 import encode
from collections.abc import Iterable
import os
import json
import sys
from app.utils.prime import prime_fetch
import copy
import pathlib

import asyncio
from app.jobs.service import JobService
from app.switch.service import SwitchService


ENV = 'prod' if os.environ.get('ENV') == 'prod' else 'test'
class MacService:
    @staticmethod
    async def get(switch_id):
        switch = SwitchService.get_by_id(switch_id)
        if switch == None:
            raise SwitchNotFound
        extra_vars = dict()
        body = dict(limit=switch.name, extra_vars=extra_vars)
        return await JobService.run_job_template_by_name('show-mac-address-table', body)

    @staticmethod
    async def find_by_mac(switches_ids, mac_or_mac_substr):
        interfaces_result = []
        macs_restults = dict()
        # Carga las macs de todos los switches pasados en switches_ids

        loop = asyncio.get_event_loop()
        loop.run_until_complete(show_mac_addr_table_multiple_sws_paralell(switches_ids, macs_restults))
        loop.close()

        # Busca entre las macs obtenidas en el paso anterior y si encuentra una devuelve en que switch e interface la encontro
        for key,value in macs_restults.items():
            for nic_name,nic_value in value.items():
                if isinstance(nic_value, Iterable):
                    if 'mac_entries' in nic_value:
                        for curr_mac in nic_value['mac_entries']:
                            if curr_mac['mac_address'].find(mac_or_mac_substr) >= 0:
                                sw = await SwitchService.get_by_id(key)
                                interfaces_result.append(dict(
                                    switch_id=sw.id,
                                    switch_name=sw.name,
                                    name=nic_name,
                                    type=curr_mac['type']))
        return interfaces_result

    @staticmethod
    async def show_mac_addr_table_multiple_sws_paralell(switches_ids, macs_restults):
        for sw_id in switches_ids:
            switch = await SwitchService.get_by_id(sw_id)
            if switch == None:
                raise SwitchNotFound
            extra_vars = dict()
            body = dict(limit=switch.name, extra_vars=extra_vars)
            macs_restults[str(sw_id)] = await JobService.run_job_template_by_name('show-mac-address-table', body)

    @staticmethod
    async def cancel_find_by_mac(switches_ids):
        for sw_id in switches_ids:
            switch = await SwitchService.get_by_id(sw_id)
            if switch == None:
                raise SwitchNotFound
            await JobService.cancel_jobs_by_template_name_and_host_name(f'{ENV}-show-mac-address-table', switch.name)
        return True

class SwitchNotFound(Exception):
    """No existe el switch"""