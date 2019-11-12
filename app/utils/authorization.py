from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError, JWTClaimsError
from functools import wraps
from app.api_response import ApiResponse

PUBLIC_KEY = os.environ.get('PUBLIC_KEY')


def authorize(func):
    @wraps(func)
    def authorize_handler(*args, **kwargs):
        token = request.headers.get('Token')
        if not token:
            return ApiResponse({"Error": "Token not found"}, 400)
        try:
            jwt.decode(token, public_key=PUBLIC_KEY, audience='account')
        except JWTError as error:
            return ApiResponse({"Error": error}, 400)
        except JWTClaimsError as error:
            return ApiResponse({"Error": error}, 400)
        except ExpiredSignatureError as error:
            return ApiResponse({"Error": error}, 400)
        return func(*args, **kwargs)
    return authorize_handler
