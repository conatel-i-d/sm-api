from flask import request
from flask_restplus import Namespace, Resource, fields
from flask.wrappers import Response

from app.api_response import ApiResponse 
from app.errors import ApiException

from .service import JobService
from .model import Job
from .interfaces import JobInterfaces



api_description = """
Representación de los Jobs de la empresa.
"""

api = Namespace('Jobs', description=api_description)
interfaces = JobInterfaces(api)

@api.route("/")
@api.response(400, 'Bad Request', interfaces.error_response_model)
@api.doc(responses={
    401: 'Unauthorized',
    403: 'Forbidden',
    500: 'Internal server error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
})
class JobResource(Resource):
    """
    Jobs Resource
    """

    @api.response(200, 'Lista de Jobs', interfaces.many_response_model)
    def get(self):
        """
        Devuelve la lista de Jobs
        """
        entities = JobService.get_all()
        return ApiResponse(interfaces.many_schema.dump(entities).data)

    @api.expect(interfaces.create_model)
    @api.response(200, 'Nuevo Job', interfaces.single_response_model)
    def post(self):
        """
        Crea un nuevo Job.
        """
        json_data = request.get_json()
        if json_data is None:
            raise ApiException('JSON body is undefined')
        body = interfaces.single_schema.load(json_data).data
        Job = JobService.create(body)
        return ApiResponse(interfaces.single_schema.dump(Job).data)


@api.route("/<int:id>")
@api.param("id", "Identificador único del Job")
@api.response(400, 'Bad Request', interfaces.error_response_model)
@api.doc(responses={
    401: 'Unauthorized',
    403: 'Forbidden',
    500: 'Internal server error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
})
class JobIdResource(Resource):
    @api.response(200, 'Job', interfaces.single_response_model)
    def get(self, id: int):
        """
        Obtiene un único Job por ID.
        """
        Job = JobService.get_by_id(id)
        return ApiResponse(interfaces.single_schema.dump(Job).data)

    @api.response(204, 'No Content')
    def delete(self, id: int) -> Response:
        """
        Elimina un único Job por ID.
        """
        from flask import jsonify

        id = JobService.delete_by_id(id)
        return ApiResponse(None, 204)

    @api.expect(interfaces.update_model)
    @api.response(200, 'Job Actualizado', interfaces.single_response_model)
    def put(self, id: int):
        """
        Actualiza un único Job por ID.
        """
        body = interfaces.single_schema.load(request.json).data
        Job = JobService.update(id, body)
        return ApiResponse(interfaces.single_schema.dump(Job).data)