from werkzeug.exceptions import HTTPException

from app.api_response import ApiResponse

class ApiException(HTTPException):
    def __init__(self, message, status=400, code='UncaughtError'):
        self.message = message
        self.status = status
        self.code = code

    def to_response(self):
        return ApiResponse(dict(message=self.message, code=self.code), status=self.status).to_response()

def register_error_handlers(app):
    app.register_error_handler(ApiException, lambda err: err.to_response())

class JobTemplateNotFound(Exception):
    """No existe el job_template"""

class PlaybookTimeout(Exception):
    """La ejecución del playbook supero el tiempo del timeout"""

class PlaybookFailure(Exception):
    """Fallo la ejecución del playbook"""

class ConnectToAwxFailure(Exception):
    """Fallo al intentar conectarse con la api de AWX"""

class PlaybookCancelFailure(Exception):
    """Fallo la intentar cancelar un job"""

class NicNotFound(Exception):
    """No existe la nic"""

class SwitchNotFound(Exception):
    """No existe el switch"""