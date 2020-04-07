import os
import sys
import json
import asyncio

from flask import request
from flask_restplus import Namespace, Resource, fields
from flask.wrappers import Response

from app.api_response import ApiResponse
from app.utils.async_action import async_action
from app.utils.authorization import authorize

from app.switch.service import SwitchService
from .service import NicsService, SwitchNotFound

from app.errors import JobTemplateNotFound, PlaybookTimeout, PlaybookFailure, ApiException

api_description = """
Representación de las nics del switch.
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
    @authorize
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
            raise ApiException('No existe un playbook para obtener la información de las interfaces')
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
    @authorize
    async def post(self, switch_id: int):
        """
        Resetea la interface indicada
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