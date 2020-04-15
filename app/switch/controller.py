import os, sys
from flask import request
from flask_restplus import Namespace, Resource, fields
from flask.wrappers import Response
from app.utils.async_action import async_action

from app.api_response import ApiResponse
from app.errors import ApiException, JobTemplateNotFound, PlaybookFailure, PlaybookTimeout, SwitchNotFound
from .service import SwitchService
from .model import Switch
from .interfaces import SwitchInterfaces

from app.utils.authorization import authorize
from app.utils.logger import log
from app.utils.b64 import decode
from app.macs.service import MacService

api_description = """
Representación de los switches de la empresa.
"""

api = Namespace('Switch', description=api_description)
interfaces = SwitchInterfaces(api)

@api.route("/")
@api.response(400, 'Bad Request', interfaces.error_response_model)
@api.doc(responses={
    401: 'Unauthorized',
    403: 'Forbidden',
    500: 'Internal server error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
})
class SwitchResource(Resource):
    """
    Switch Resource
    """
    @api.response(200, 'Lista de Switches', interfaces.many_response_model)
    @async_action
    @authorize
    async def get(self):
        """
        Devuelve la lista de Switches
        """
        try:
            entities = await SwitchService.get_all()
            return ApiResponse(interfaces.many_schema.dump(entities).data)
        except JobTemplateNotFound:
            raise ApiException('No existe un playbook para obtener la infrmación de las interfaces')
        except PlaybookTimeout:
            raise ApiException('La ejecución de la tarea supero el tiempo del timeout')
        except PlaybookFailure:
            raise ApiException('Fallo la ejecución de la tarea')
    @api.expect(interfaces.create_model)
    @api.response(200, 'Nuevo Switch', interfaces.single_response_model)
    @log
    @authorize
    def post(self):
        """
        Crea un nuevo Switch.
        """
        json_data = request.get_json()
        if json_data is None:
            raise ApiException('JSON body is undefined')
        body = interfaces.single_schema.load(json_data).data
        Switch = SwitchService.create(body)
        return ApiResponse(interfaces.single_schema.dump(Switch).data)

    @api.expect(interfaces.update_model)
    @api.response(200, 'Switches Actualizados', interfaces.many_response_model)
    @log
    @authorize
    def put(self, id: int):
        """
        Actualiza un batch de Switches por su ID.
        """
        json_data = request.get_json()
        sw_updated = []
        for item in json_data:
            sw = interfaces.single_schema.load(request.json).data
            sw_updated.append(SwitchService.update(id, sw))
        return ApiResponse(interfaces.many_schema.dump(sw_updated).data)

@api.route("/<int:id>")
@api.param("id", "Identificador único del Switch")
@api.response(400, 'Bad Request', interfaces.error_response_model)
@api.doc(responses={
    401: 'Unauthorized',
    403: 'Forbidden',
    500: 'Internal server error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
})
class SwitchIdResource(Resource):
    @api.response(200, 'Switch', interfaces.single_response_model)
    @async_action
    @authorize
    async def get(self, id: int):
        """
        Obtiene un único Switch por ID.
        """
        try:
            switch = await SwitchService.get_by_id(id)
            return ApiResponse(interfaces.single_schema.dump(switch).data)
        except SwitchNotFound:
            raise ApiException(f'No se encuentra un switch con el id:{id}')
        except JobTemplateNotFound:
            raise ApiException('No existe un playbook para obtener la infrmación de las interfaces')
        except PlaybookTimeout:
            raise ApiException('La ejecución de la tarea supero el tiempo del timeout')
        except PlaybookFailure:
            raise ApiException('Fallo la ejecución de la tarea')


    @api.response(204, 'No Content')
    @log
    @authorize
    def delete(self, id: int) -> Response:
        """
        Elimina un único Switch por ID.
        """
        from flask import jsonify
        id = SwitchService.delete_by_id(id)
        return ApiResponse(None, 204)

    @api.expect(interfaces.update_model)
    @api.response(200, 'Switch Actualizado', interfaces.single_response_model)
    @log
    @authorize
    def put(self, id: int):
        """
        Actualiza un único Switch por ID.
        """
        try:
            body = interfaces.single_schema.load(request.json).data
            Switch = SwitchService.update(id, body)
            return ApiResponse(interfaces.single_schema.dump(Switch).data)
        except SwitchNotFound:
            raise ApiException(f'No se encuentra un switch con el id:{id}')
@api.route("/inventory")
@api.response(400, 'Bad Request', interfaces.error_response_model)
@api.doc(responses={
    401: 'Unauthorized',
    403: 'Forbidden',
    500: 'Internal server error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
})
class SwitchInventoryResource(Resource):
    """
    Inventory switch Resource
    """
    @api.response(200, 'Inventario con lista de swithces')
    @async_action
    async def get(self):
        """
        Devuelve la lista de Switches
        """
        try:
            entities = await SwitchService.get_all()
            ansible_switches_vars = {}
            for x  in entities:
                ansible_switches_vars[x.name] = { 
                    "ansible_host": x.ip,
                    "ansible_become": True,
                    "ansible_become_method": "enable",
                    "ansible_connection": "network_cli",
                    "ansible_network_os": "ios",
                    "ansible_port": x.ansible_ssh_port or 22,
                    "ansible_user": decode(x.ansible_user),
                    "ansible_ssh_pass": decode(x.ansible_ssh_pass)
                }
            ansible_switches_hostnames = map(lambda x : x.name, entities)
            sw_inv = {
                'group': {
                    'hosts': list(ansible_switches_hostnames),
                },
                '_meta': {
                    'hostvars': ansible_switches_vars
                }
            }
            return ApiResponse(sw_inv)
        except JobTemplateNotFound:
            raise ApiException('No existe un playbook para obtener la infrmación de las interfaces')
        except PlaybookTimeout:
            raise ApiException('La ejecución de la tarea supero el tiempo del timeout')
        except PlaybookFailure:
            raise ApiException('Fallo la ejecución de la tarea')

@api.route("/<int:id>/macs")
@api.param("id", "Identificador único del Switch")
class SwitchMacResource(Resource):
    """
    Mac Resource
    """
    @api.response(200, 'Lista de Interfaces con sus respectivas macs', interfaces.many_response_model)
    @async_action
    @authorize
    async def get(self, switch_id: int):
        """
        Devuelve la lista de todaslas macs del switch
        """
        try:
            resp = await MacService.get(switch_id)
            return ApiResponse(resp)
        except SwitchNotFound:
            raise ApiException(f'No se encuentra un switch con el id:{switch_id}')
        except JobTemplateNotFound:
            raise ApiException('No existe un playbook para obtener la infrmación de las interfaces')
        except PlaybookTimeout:
            raise ApiException('La ejecución de la tarea supero el tiempo del timeout')
        except PlaybookFailure:
            raise ApiException('Fallo la ejecución de la tarea')
