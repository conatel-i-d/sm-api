import os
import json

from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError, JWTClaimsError, JWKError
from functools import wraps
from flask import request
from app.api_response import ApiResponse



PUBLIC_KEY = f"""
-----BEGIN PUBLIC KEY----- 
{os.environ.get('PUBLIC_KEY')}
-----END PUBLIC KEY-----
"""



def authorize(func):
    @wraps(func)
    def authorize_handler(*args, **kwargs):
        token = request.headers.get('Token')
        if not token:
            return ApiResponse({"Error": "Token not found"}, 400)
        try:
            jwt.decode(token, PUBLIC_KEY, algorithms=['RS256'], audience='dashboard')
        except JWTError as error:
            return ApiResponse({"Error": str(error)}, 400)
        except JWTClaimsError as error:
            return ApiResponse({"Error": str(error)}, 400)
        except ExpiredSignatureError as error:
            return ApiResponse({"Error": str(error)}, 400)
        except JWKError as error:
            return ApiResponse({"Error": str(error)}, 400)
        return func(*args, **kwargs)
    return authorize_handler
