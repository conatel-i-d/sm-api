from flask import request
from flask_restplus import Namespace, Resource, fields
from flask.wrappers import Response

from app.api_response import ApiResponse
from app.errors import ApiException
from .service import LogService
from .model import Log
from .interfaces import LogInterfaces

from app.utils.authorization import authorize

api_description = """
Representación de los switches de la empresa.
"""

api = Namespace('Log', description=api_description)
interfaces = LogInterfaces(api)

@api.route("/")
@api.response(400, 'Bad Request', interfaces.error_response_model)
@api.doc(responses={
    401: 'Unauthorized',
    403: 'Forbidden',
    500: 'Internal server error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
})
class LogResource(Resource):
    """
    Log Resource
    """

    @api.response(200, 'Lista de Logs', interfaces.many_response_model)
    @authorize
    def get(self):
        """
        Devuelve la lista de Logs
        """
        entities = LogService.get_all()
        return ApiResponse(interfaces.many_schema.dump(entities).data)

    @api.expect(interfaces.create_model)
    @api.response(200, 'Nuevo Log', interfaces.single_response_model)
    @authorize
    def post(self):
        """
        Crea un nuevo Log.
        """
        json_data = request.get_json()
        if json_data is None:
            raise ApiException('JSON body is undefined')
        body = interfaces.single_schema.load(json_data).data
        Log = LogService.create(body)
        return ApiResponse(interfaces.single_schema.dump(Log).data)


@api.route("/<int:id>")
@api.param("id", "Identificador único del Log")
@api.response(400, 'Bad Request', interfaces.error_response_model)
@api.doc(responses={
    401: 'Unauthorized',
    403: 'Forbidden',
    500: 'Internal server error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
})
class LogIdResource(Resource):
    @api.response(200, 'Log', interfaces.single_response_model)
    @authorize
    def get(self, id: int):
        """
        Obtiene un único Log por ID.
        """
        Log = LogService.get_by_id(id)
        return ApiResponse(interfaces.single_schema.dump(Log).data)

    @api.response(204, 'No Content')
    @authorize
    def delete(self, id: int) -> Response:
        """
        Elimina un único Log por ID.
        """
        id = LogService.delete_by_id(id)
        return ApiResponse(None, 204)

    @api.expect(interfaces.update_model)
    @api.response(200, 'Log Actualizado', interfaces.single_response_model)
    @authorize
    def put(self, id: int):
        """
        Actualiza un único Log por ID.
        """
        body = interfaces.single_schema.load(request.json).data
        Log = LogService.update(id, body)
        return ApiResponse(interfaces.single_schema.dump(Log).data)