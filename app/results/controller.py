from flask import request
from flask_restplus import Namespace, Resource, fields
from flask.wrappers import Response

from app.api_response import ApiResponse
from .service import ResultService
from .model import Result
from .interfaces import ResultInterfaces

api_description = """
Representación de los Results de la empresa.
"""

api = Namespace('Results', description=api_description)
interfaces = ResultInterfaces(api)

@api.route("/")
@api.response(400, 'Bad Request', interfaces.error_response_model)
@api.doc(responses={
    401: 'Unauthorized',
    403: 'Forbidden',
    500: 'Internal server error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
})
class ResultResource(Resource):
    """
    Results Resource
    """

    @api.response(200, 'Lista de Results', interfaces.many_response_model)
    def get(self):
        """
        Devuelve la lista de Results
        """
        entities = ResultService.get_all()
        return ApiResponse(interfaces.many_schema.dump(entities).data)

    @api.expect(interfaces.create_model)
    @api.response(200, 'Nuevo Result', interfaces.single_response_model)
    def post(self):
        """
        Crea un nuevo Result.
        """
        json_data = request.get_json()
        if json_data is None:
            raise Exception('JSON body is undefined')
        body = interfaces.single_schema.load(json_data).data
        Result = ResultService.create(body)
        return ApiResponse(interfaces.single_schema.dump(Result).data)


@api.route("/<int:id>")
@api.param("id", "Identificador único del Result")
@api.response(400, 'Bad Request', interfaces.error_response_model)
@api.doc(responses={
    401: 'Unauthorized',
    403: 'Forbidden',
    500: 'Internal server error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
})
class ResultIdResource(Resource):
    @api.response(200, 'Result', interfaces.single_response_model)
    def get(self, id: int):
        """
        Obtiene un único Result por ID.
        """
        Result = ResultService.get_by_id(id)
        return ApiResponse(interfaces.single_schema.dump(Result).data)

    @api.response(204, 'No Content')
    def delete(self, id: int) -> Response:
        """
        Elimina un único Result por ID.
        """
        from flask import jsonify

        id = ResultService.delete_by_id(id)
        return ApiResponse(None, 204)

    @api.expect(interfaces.update_model)
    @api.response(200, 'Result Actualizado', interfaces.single_response_model)
    def put(self, id: int):
        """
        Actualiza un único Result por ID.
        """
        body = interfaces.single_schema.load(request.json).data
        Result = ResultService.update(id, body)
        return ApiResponse(interfaces.single_schema.dump(Result).data)