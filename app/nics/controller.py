from flask import request
from flask_restplus import Namespace, Resource, fields
from flask.wrappers import Response
from .task import get_nics
from app.api_response import ApiResponse
# from .interfaces import SwitchInterfaces

api_description = """
Representación de los switches de la empresa.
"""

api = Namespace('Nics', description=api_description)

@api.route("/")
# @api.response(400, 'Bad Request', interfaces.error_response_model)
# @api.doc(responses={
#     401: 'Unauthorized',
#     403: 'Forbidden',
#     500: 'Internal server error',
#     502: 'Bad Gateway',
#     503: 'Service Unavailable',
# })
class InterfaceResource(Resource):
    """
    Interface Resource
    """


    # @api.response(200, 'Lista de Interfaces', interfaces.many_response_model)
    def get(self):
        """
        Devuelve la lista de Interfaces
        """
        task = get_nics.delay()
        async_result = get_nics.async_result(id=task.id)
        return ApiResponse({ "hola": async_result }) #async_result

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