from app.utils.base_interfaces_test import BaseInterfaces, marshmallow_fields, restplus_fields

class ResultInterfaces(BaseInterfaces):
    __name__ = 'Result'
    id = dict(
        m=marshmallow_fields.Int(attribute='id', dump_only=True),
        r=restplus_fields.Integer(description='Identificador único', required=True, example=123),
    )
    type = dict(
        m=marshmallow_fields.String(attribute='type'),
        r=restplus_fields.String(description='Tipo de resultado', required=True, example='interfaces'),
    )
    result = dict(
        m=marshmallow_fields.String(attribute='result'),
        r=restplus_fields.String(description='El resultado', required=False, example='{ interfaces: [ nic1: ..., nic: ...] }'),
    )
    create_model_keys = ['name', 'type', 'result']
    update_model_keys = ['type', 'result']