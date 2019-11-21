import os
import sys
import json
import asyncio
from flask import request
from flask_restplus import Namespace, Resource, fields
from flask.wrappers import Response
from app.errors import ApiException
from app.api_response import ApiResponse
from app.utils.async_action import async_action
from app.switch.service import SwitchService
from app.results.service import ResultService
from .service import NicsService, SwitchNotFound
from app.utils.awx import JobTemplateNotFound, PlaybookTimeout, PlaybookFailure

api_description = """
Representación de los switches de la empresa.
"""

api = Namespace('Nics', description=api_description)

@api.route("/<int:switch_id>/nics")
@api.param("switch_id", "Identificador único del Switch")
class InterfaceResource(Resource):
    """
    Interface Resource
    """


    # @api.response(200, 'Lista de Interfaces', interfaces.many_response_model)

    @async_action
    async def get(self, switch_id: int):
        """
        Devuelve la lista de Interfaces
        """
        # List jobs templates
        # '/api/v2/job_templates/'
        try:
            result = await NicsService.get_by_switch_id(switch_id)
            return ApiResponse(result)
            #return ApiResponse(RESULT)
        except SwitchNotFound:
            raise ApiException(f'No se encuentra un switch con el id:{switch_id}')
        except JobTemplateNotFound:
            raise ApiException('No existe un playbook para obtener la infrmación de las interfaces')
        except PlaybookTimeout:
            raise ApiException('La ejecución de la tarea supero el tiempo del timeout')
        except PlaybookFailure:
            raise ApiException('Fallo la ejecución de la tarea')

@api.route("/<int:switch_id>/nics/reset")
@api.param("switch_id", "Identificador único del Switch")
class InterfaceResource(Resource):
    """
    Interface Resource
    """
    @async_action
    async def post(self, switch_id: int):
        """
        Devuelve la lista de Interfaces
        """
        try:
            nic_name = request.args.get('nic_name')
            result = await NicsService.reset_switch_nic(switch_id, nic_name)
            return ApiResponse(result)
        except SwitchNotFound:
            raise ApiException(f'No se encuentra un switch con el id:{switch_id}')
        except JobTemplateNotFound:
            raise ApiException('No existe un playbook para obtener la infrmación de las interfaces')
        except PlaybookTimeout:
            raise ApiException('La ejecución de la tarea supero el tiempo del timeout')
        except PlaybookFailure:
            raise ApiException('Fallo la ejecución de la tarea')


#     @api.expect(interfaces.create_model)
#     @api.response(200, 'Nuevo Switch', interfaces.single_response_model)
#     def post(self):
#         """
#         Crea un nuevo Switch.
#         """
#         json_data = request.get_json()
#         if json_data is None:
#             raise Exception('JSON body is undefined')
#         body = interfaces.single_schema.load(json_data).data
#         Switch = SwitchService.create(body)
#         return ApiResponse(interfaces.single_schema.dump(Switch).data)


# @api.route("/<int:id>")
# @api.param("id", "Identificador único del Switch")
# @api.response(400, 'Bad Request', interfaces.error_response_model)
# @api.doc(responses={
#     401: 'Unauthorized',
#     403: 'Forbidden',
#     500: 'Internal server error',
#     502: 'Bad Gateway',
#     503: 'Service Unavailable',
# })
# class SwitchIdResource(Resource):
#     @api.response(200, 'Switch', interfaces.single_response_model)
#     def get(self, id: int):
#         """
#         Obtiene un único Switch por ID.
#         """
#         Switch = SwitchService.get_by_id(id)
#         return ApiResponse(interfaces.single_schema.dump(Switch).data)

#     @api.response(204, 'No Content')
#     def delete(self, id: int) -> Response:
#         """
#         Elimina un único Switch por ID.
#         """
#         from flask import jsonify

#         id = SwitchService.delete_by_id(id)
#         return ApiResponse(None, 204)

#     @api.expect(interfaces.update_model)
#     @api.response(200, 'Switch Actualizado', interfaces.single_response_model)
#     def put(self, id: int):
#         """
#         Actualiza un único Switch por ID.
#         """
#         body = interfaces.single_schema.load(request.json).data
#         Switch = SwitchService.update(id, body)
#         return ApiResponse(interfaces.single_schema.dump(Switch).data)