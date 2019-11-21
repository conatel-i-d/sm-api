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