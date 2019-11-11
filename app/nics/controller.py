from flask import request
from flask_restplus import Namespace, Resource, fields
from flask.wrappers import Response
from app.api_response import ApiResponse
#async dependencies
from app.utils.async_action import async_action
from app.utils.awx import awx_fetch, awx_post
from app.switch.service import SwitchService
from app.results.service import ResultService
import asyncio
import aiohttp
import json
import os

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
            switch = SwitchService.get_by_id(switch_id)
            if (switch == None):
                return ApiResponse({ "Error": 'Switch not found'}, 400)
            else:
                result = await awx_fetch('/api/v2/job_templates/')
                templates =  result["results"]
                template = None
                if (os.environ.get('ENV') == 'prod'):
                    templateList = list(filter(lambda x: x["name"] == "prod-show-interfaces-information", templates))
                    if (len(templateList) > 0):
                        template = templateList[0]
                else:
                    templateList = list(filter(lambda x: x["name"] == "test-show-interfaces-information", templates))
                    if (len(templateList) > 0):
                        template = templateList[0]
                
                if (template != None):
                    launch_result = await awx_post('/api/v2/job_templates/' + str(template["id"]) + '/launch/',
                    { 
                        "limit": switch.name
                    })
                    job_id = launch_result["job"]
                else:
                    return ApiResponse({ "Error": 'The template ' + os.environ.get('ENV')  + '-show-interfaces-information not found'}, 400)
                
                for i in range(15):
                    job_status_result = await awx_fetch('/api/v2/jobs/' + str(job_id) + '/')
                    if (job_status_result["status"] == "failed"):
                        return ApiResponse({ "Error": "Playbook execution error" }, 400)
                    if (job_status_result["status"] == "successful"):
                        rcv_result = ResultService.get({ "job_id": job_id })
                        if (rcv_result != None):
                            ResultService.delete_by_id(rcv_result.id)
                            return ApiResponse(rcv_result.result)
                    # elif (job_status_result["status"] != "waiting" and job_status_result["status"] != "running"):
                    #     return ApiResponse({ "Error": "Job status unrecognized" }, 400)
                    await asyncio.sleep(2)
                return ApiResponse({ "Error": "Playbook execution timeout error" }, 400)
        except Exception as e:
            return ApiResponse({ "Error": str(e) }, 400)
            


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