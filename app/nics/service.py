"""
Nics service

Desacopla el manejo del request/response HTTP de la lógica de la
aplicación.
"""
import asyncio
from app.switch.service import SwitchService
from app.jobs.service import JobService

class NicsService:
    @staticmethod
    async def reset_switch_nic(switch_id, nic_name):
        switch = SwitchService.get_by_id(switch_id)
        if switch == None:
            raise SwitchNotFound
        extra_vars = dict(interface_name=nic_name)
        body = dict(limit=switch.name, extra_vars=extra_vars)
        return await JobService.run_job_template_by_name('reset-interface', body)


    @staticmethod
    async def get_by_switch_id(switch_id):
        """
        Devuelve la información de todas las interfaces a través
        del AWX, quien consulta directamente al switch.
        
        Args:
        switch_id (int): Identidad del switch
        """
        switch = SwitchService.get_by_id(switch_id)
        if switch == None:
            raise SwitchNotFound
        extra_vars = dict(something='awesome')
        body = dict(limit=switch.name, extra_vars=extra_vars)
        result = await JobService.run_job_template_by_name('show-interfaces-information', body)
        return result


class SwitchNotFound(Exception):
    """No existe el switch"""
