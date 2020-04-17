"""
Nics service

Desacopla el manejo del request/response HTTP de la lógica de la
aplicación.
"""
import asyncio
from app.switch.service import SwitchService
from app.jobs.service import JobService
from app.utils.prime import prime_fetch
from app.errors import ApiException, SwitchNotFound


class NicsService:
    @staticmethod
    async def reset_switch_nic(switch_id, nic_name):
        switch = await SwitchService.get_by_id(switch_id)
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
        switch = await SwitchService.get_by_id(switch_id)
        if switch == None:
            raise SwitchNotFound
        extra_vars = dict(something='awesome')
        body = dict(limit=switch.name, extra_vars=extra_vars)
        sw_result = await JobService.run_job_template_by_name('show-interfaces-information', body)
        try:
            prime_result = await NicsService.get_from_prime_by_switch_id(switch_id)
            prime_result.update(sw_result)
            print(f'prime result {prime_result}', flush=True)
            return prime_result
        except Exception as err:
            print("Switch no pertenece al prime", flush=True)
            print(str(err), flush=True)
        return sw_result

    @staticmethod
    async def get_from_prime_by_switch_id(switch_id):
        """
        Devuelve la información de todas las interfaces a través
        del la api del Cisco Prime, quien consulta directamente al switch.

        Args:
        switch_id (int): Identidad del switch
        """
        result = dict()
        try:
            from_prime = await prime_fetch(f'/webacs/api/v4/data/InventoryDetails/{switch_id}.json')
            for interface in from_prime['queryResponse']["entity"][0]["inventoryDetailsDTO"]["ethernetInterfaces"]["ethernetInterface"]:
                result[interface["name"]] = interface
            return result
        except Exception as err:
            print("Error in get_from_prime: " + str(err), flush=True)
            raise ApiException("Error al cargar nics del Cisco Prime. Error: " + str(err))