from app.utils.base_interfaces import BaseInterfaces, marshmallow_fields, restplus_fields

class SwitchInterfaces(BaseInterfaces):
    __name__ = 'Switch'
    id = dict(
        m=marshmallow_fields.Int(attribute='id', dump_only=True),
        r=restplus_fields.Integer(description='Identificador único', required=True, example=123),
    )
    name = dict(
        m=marshmallow_fields.String(attribute='name'),
        r=restplus_fields.String(description='Nombre del Switch', required=True, example='sw-core-1'),
    )
    description = dict(
        m=marshmallow_fields.String(attribute='description'),
        r=restplus_fields.String(description='Descripción del Switch', required=False, example='Switch de core #1'),
    )
    model = dict(
        m=marshmallow_fields.String(attribute='model'),
        r=restplus_fields.String(
            description='Modelo del Switch',
            required=False,
            example='Cisco 2960x'    
        )
    )
    ip = dict(
        m=marshmallow_fields.String(attribute='ip'),
        r=restplus_fields.String(
            description='Dirección IP para la administración del switch',
            required=True,
            example='192.168.1.1'    
        )
    )
    ansible_user = dict(
        m=marshmallow_fields.String(attribute='ansible_user'),
        r=restplus_fields.String(
            description='Nombre del usuario para conectarse ssh',
            required=False,
            example='my_name'    
        )
    )
    ansible_ssh_pass = dict(
        m=marshmallow_fields.String(attribute='ansible_ssh_pass'),
        r=restplus_fields.String(
            description='Password del usuario para conectarse ssh',
            required=False,
            example='my_pass'    
        )
    )

    ansible_ssh_port = dict(
        m=marshmallow_fields.Int(attribute='ansible_ssh_port'),
        r=restplus_fields.Integer(description='Puerto pasa conectarse por ssh', required=False, example=22),
    )
    is_visible = dict(
        m=marshmallow_fields.Boolean(attribute='is_visible'),
        r=restplus_fields.Boolean(description='Determina si el switch es visible para el operador', required=False, example=False),
    )

    create_model_keys = ['name', 'description', 'model', 'ip', 'ansible_user', 'ansible_ssh_pass', 'ansible_ssh_port', 'is_visible' ]
    update_model_keys = ['name', 'description', 'model', 'ip', 'ansible_user', 'ansible_ssh_pass', 'ansible_ssh_port', 'is_visible' ]