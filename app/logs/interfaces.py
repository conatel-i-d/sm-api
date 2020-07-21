from app.utils.base_interfaces import BaseInterfaces, marshmallow_fields, restplus_fields

class LogInterfaces(BaseInterfaces):
    __name__ = 'Log'
    id = dict(
        m=marshmallow_fields.Int(attribute='id', dump_only=True),
        r=restplus_fields.Integer(description='Identificador único', required=True, example=123),
    )
    http_method = dict(
        m=marshmallow_fields.String(attribute='http_method'),
        r=restplus_fields.String(description='Tipo de metodo http', required=True, example='POST'),
    )
    http_url = dict(
        m=marshmallow_fields.String(attribute='http_url'),
        r=restplus_fields.String(description='url de destino', required=False, example='http://ejemplo.com/api/entidad/'),
    )
    payload = dict(
        m=marshmallow_fields.String(attribute='payload'),
        r=restplus_fields.String(
            description='Payload del Request',
            required=False,
            example='{ "name": "Juan"}'    
        )
    )

    user_name = dict(
        m=marshmallow_fields.String(attribute='user_name'),
        r=restplus_fields.String(description='nombre de usuario', required=True, example='nombre de ejemplo'),
    )
    user_email = dict(
        m=marshmallow_fields.String(attribute='user_email'),
        r=restplus_fields.String(description='email de usuario', required=True, example='email@de.ejemplo.com'),
    )
    response_status_code = dict(
        m=marshmallow_fields.Int(attribute='response_status_code', dump_only=True),
        r=restplus_fields.Integer(description='Http status code de la respuesta', required=True, example=123),
    )
    message = dict(
        m=marshmallow_fields.String(attribute='message', dump_only=True),
        r=restplus_fields.String(description='Mensaje de la respuesta', required=True, example=123),
    )
    date_start = dict(
        m=marshmallow_fields.String(attribute='date_start'),
        r=restplus_fields.String(description='Datetime de inicio la consulta', required=True, example='2018-28-01 00:00:00'),
    )
    date_end = dict(
        m=marshmallow_fields.String(attribute='date_end'),
        r=restplus_fields.String(description='Datetime de finalizacion la consulta', required=True, example='2018-28-01 00:00:00'),
    )
    create_model_keys = ["id", "http_method", "http_url", "payload", "user_name", "user_email", "response_status_code", "message", "date_start", "date_end"]
    update_model_keys = ["id", "http_method", "http_url", "payload", "user_name", "user_email", "response_status_code", "message", "date_start", "date_end"]