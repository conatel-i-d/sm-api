from flask import request
from flask_restplus import Namespace, Resource, fields
from flask.wrappers import Response

from app.api_response import ApiResponse
from .service import ResultService
from .model import Result
from .interfaces import ResultInterfaces

api_description = """
Representación de los switches de la empresa.
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
class SwitchResource(Resource):
    """
    Results Resource
    """

    @api.response(200, 'Lista de Switches', interfaces.many_response_model)
    def get(self):
        """
        Devuelve la lista de Switches
        """
        entities = ResultService.get_all()
        return ApiResponse(interfaces.many_schema.dump(entities).data)

    @api.expect(interfaces.create_model)
    @api.response(200, 'Nuevo Switch', interfaces.single_response_model)
    def post(self):
        """
        Crea un nuevo Switch.
        """
        json_data = request.get_json()
        if json_data is None:
            raise Exception('JSON body is undefined')
        body = interfaces.single_schema.load(json_data).data
        Switch = SwitchService.create(body)
        return ApiResponse(interfaces.single_schema.dump(Switch).data)


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
    def get(self, id: int):
        """
        Obtiene un único Switch por ID.
        """
        Switch = SwitchService.get_by_id(id)
        return ApiResponse(interfaces.single_schema.dump(Switch).data)

    @api.response(204, 'No Content')
    def delete(self, id: int) -> Response:
        """
        Elimina un único Switch por ID.
        """
        from flask import jsonify

        id = SwitchService.delete_by_id(id)
        return ApiResponse(None, 204)

    @api.expect(interfaces.update_model)
    @api.response(200, 'Switch Actualizado', interfaces.single_response_model)
    def put(self, id: int):
        """
        Actualiza un único Switch por ID.
        """
        body = interfaces.single_schema.load(request.json).data
        Switch = SwitchService.update(id, body)
        return ApiResponse(interfaces.single_schema.dump(Switch).data)