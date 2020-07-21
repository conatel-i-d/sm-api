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

from app.errors import ApiException

ENV = 'prod' if os.environ.get('ENV') == 'prod' else 'test'
class MacService:
    @staticmethod
    async def get(switch_id):
        switch = await SwitchService.get_by_id(switch_id)
        if switch == None:
            raise ApiException(f'No se encuentra el switch con el id {switch_id}', 404)
        extra_vars = dict()
        body = dict(limit=switch.name, extra_vars=extra_vars)
        return await JobService.run_job_template_by_name('show-mac-address-table', body)

    @staticmethod
    async def show_mac_addr_table(switch, macs_results):
        extra_vars = dict()
        body = dict(limit=switch["name"], extra_vars=extra_vars)
        macs_results.append({ 
            "id": switch["id"],
            "name": switch["name"],
            "interfaces": await JobService.run_job_template_by_name('show-mac-address-table', body)
        })
        return True

    @staticmethod
    async def find_by_mac(switches_ids):
        macs_results = []
        switches = []
        # Carga las macs de todos los switches pasados en switches_ids
        for sw_id in switches_ids:
            switch = await SwitchService.get_by_id(sw_id)
            if switch == None:
                raise ApiException(f'No se encuentra el switch con el id {sw_id}', 404)
            else:
                switches.append({ "id": sw_id, "name": switch.name})
        await asyncio.gather(*[MacService.show_mac_addr_table(sw, macs_results) for sw in switches])
        return macs_results
        

    @staticmethod
    async def cancel_find_by_mac(switches_ids):
        for sw_id in switches_ids:
            switch = await SwitchService.get_by_id(sw_id)
            if switch == None:
                raise ApiException(f'No se encuentra el switch con el id {sw_id}', 404)
            await JobService.cancel_jobs_by_template_name_and_host_name(f'{ENV}-show-mac-address-table', switch.name)
        return True