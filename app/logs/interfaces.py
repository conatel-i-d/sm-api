from app.utils.base_interfaces import BaseInterfaces, marshmallow_fields, restplus_fields

class LogInterfaces(BaseInterfaces):
    __name__ = 'Log'
    id = dict(
        m=marshmallow_fields.Int(attribute='id', dump_only=True),
        r=restplus_fields.Integer(description='Identificador único', required=True, example=123),
    )
    event_type = dict(
        m=marshmallow_fields.String(attribute='event_type'),
        r=restplus_fields.String(description='Nombre del Evento', required=True, example='POST'),
    )
    event_result = dict(
        m=marshmallow_fields.String(attribute='event_result'),
        r=restplus_fields.String(description='Resultado del evento', required=True, example='SUCCESS'),
    )
    entity = dict(
        m=marshmallow_fields.String(attribute='entity'),
        r=restplus_fields.String(description='Entidad a la que se le realizo el cambio', required=True, example='Switches'),
    )
    payload = dict(
        m=marshmallow_fields.String(attribute='payload'),
        r=restplus_fields.String(
            description='Payload del Request',
            required=False,
            example='{ "name": "Juan"}'    
        )
    )
    user_id = dict(
        m=marshmallow_fields.String(attribute='user_id'),
        r=restplus_fields.String(description='Usuario que emitio el request', required=True, example='asdas-asda12easd-asdasdasd-asda'),
    )
    date = dict(
        m=marshmallow_fields.String(attribute='date'),
        r=restplus_fields.String(description='Fecha de emitida la consulta', required=True, example='2018-28-01 00:00:00'),
    )
    create_model_keys = ['event_type', 'entity', 'payload', 'user_id', 'date']
    update_model_keys = ['event_type', 'entity', 'payload', 'user_id', 'date']