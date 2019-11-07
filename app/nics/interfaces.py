# from app.utils.base_interfaces_test import BaseInterfaces, marshmallow_fields, restplus_fields

# class SwitchInterfaces(BaseInterfaces):
#     __name__ = 'Switch'
#     id = dict(
#         m=marshmallow_fields.Int(attribute='id', dump_only=True),
#         r=restplus_fields.Integer(description='Identificador único', required=True, example=123),
#     )
#     name = dict(
#         m=marshmallow_fields.String(attribute='name'),
#         r=restplus_fields.String(description='Nombre del Switch', required=True, example='sw-core-1'),
#     )
#     description = dict(
#         m=marshmallow_fields.String(attribute='description'),
#         r=restplus_fields.String(description='Descripción del Switch', required=False, example='Switch de core #1'),
#     )
#     model = dict(
#         m=marshmallow_fields.String(attribute='model'),
#         r=restplus_fields.String(
#             description='Modelo del Switch',
#             required=False,
#             example='Cisco 2960x'    
#         )
#     )
#     ip = dict(
#         m=marshmallow_fields.String(attribute='ip'),
#         r=restplus_fields.String(
#             description='Dirección IP para la administración del switch',
#             required=True,
#             example='192.168.1.1'    
#         )
#     )
#     create_model_keys = ['name', 'description', 'model', 'ip']
#     update_model_keys = ['name', 'description', 'model', 'ip']