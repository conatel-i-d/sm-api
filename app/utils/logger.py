import os
import json
import datetime
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError, JWTClaimsError, JWKError
from functools import wraps
from flask import request, redirect, Response, make_response
from app.api_response import ApiResponse
from app.errors import ApiException

PUBLIC_KEY = f"""
-----BEGIN PUBLIC KEY----- 
{os.environ.get('PUBLIC_KEY')}
-----END PUBLIC KEY-----
"""


def log(func):
    @wraps(func)
    def log_handler(*args, **kwargs):
        token = request.headers.get('Token')
        if not token:
            return ApiResponse({"Error": "Token not found"}, 400)
        http_method = request.method
        http_url = request.url
        payload = json.dumps(request.get_json())

        token_dec = jwt.decode(token, PUBLIC_KEY, algorithms=['RS256'], audience='dashboard', options={
            "verify_signature": False,
            "verify_aud": False,
            "verify_iat": False,
            "verify_exp": False,
            "verify_nbf": False,
            "verify_iss": False,
            "verify_sub": False,
            "verify_jti": False,
            "verify_at_hash": False
        })        
        user_name = token_dec["name"]
        user_email = token_dec["email"]
        date_start = datetime.datetime.now()  
        try:
            response = func(*args, **kwargs)
        except ApiException as err:
            response = err
        except Exception as err:
            response = ApiException('Internal server error', 500, str(err))

        if isinstance(response, ApiResponse):
            response_status_code = response.status
            message = str(response.value or "")[0:250] + "..."
        elif isinstance(response, ApiException):
          if response.status == 500:
            message = f'message: {response.message}, code: {response.code}'
          else:
            message = response.message 
          response_status_code = response.status
          response = ApiResponse(message, response_status_code)
        date_end = datetime.datetime.now()
        print({
          "http_method": http_method,
          "http_url": http_url,
          "payload": payload,
          "user_name": user_name,
          "user_email": user_email,
          "date_start": date_start,
          "response_status_code": response_status_code,
          "message": message,
          "date_end": date_end
        },flush=True)
        return response
    return log_handler
