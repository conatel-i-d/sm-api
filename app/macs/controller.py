import os, sys
from flask import request
from flask_restplus import Namespace, Resource, fields
from flask.wrappers import Response
from app.utils.async_action import async_action

from app.api_response import ApiResponse
from app.errors import ApiException
from .service import MacService
from app.utils.authorization import authorize 
from app.utils.b64 import decode

api_description = """
Methodos find y cancel_find para las macs de un switch o edificio.
"""

api = Namespace('Macs', description=api_description)

@api.route("/find")
@api.response(400, 'Bad Request')
@api.doc(responses={
    401: 'Unauthorized',
    403: 'Forbidden',
    500: 'Internal server error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
})
class FindMacResource(Resource):
    
    @api.expect([str])
    @api.response(200, 'Interfaces donde se encontro la mac')
    @authorize
    @async_action
    async def post(self):
        """
        Busca una mac o substring de la misma en la lista de swtiches recibidos en el body.
        """
        json_data = request.get_json()
        if json_data is None:
            raise ApiException('JSON body is undefined')
        switches_ids = list(json_data["switchesToFindIds"])
        resp = await MacService.find_by_mac(switches_ids)
        return ApiResponse(resp)


@api.route("/cancel_find_tasks")
@api.response(400, 'Bad Request')
@api.doc(responses={
    401: 'Unauthorized',
    403: 'Forbidden',
    500: 'Internal server error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
})
class CancelFindMacResource(Resource):
    @api.expect([str])
    @api.response(201, 'Trabajos de buscar mac cancelados correctamente')
    @authorize
    @async_action
    async def post(self):
        """
        Dados una lista de ids de swithces, busca los trabajos "busqueda de mac" pendientes en esos switches y los cancela.
        """
        json_data = request.get_json()
        if json_data is None:
            raise ApiException('JSON body is undefined')
        switches_ids = list(json_data["switchesToFindIds"])
        resp = await MacService.cancel_find_by_mac(switches_ids)
        return ApiResponse({}, 201)