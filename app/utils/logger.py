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
        now_datetime = datetime.datetime.now()
        print("user_name", user_name, flush=True)
        print("user_email", user_email, flush=True)
        print("now_datetime", now_datetime, flush=True)  
        result, status_code = func(*args, **kwargs)
        print("result", result, flush=True)
        print("status_code", status_code, flush=True)
        return make_response(result, status_code)
    return log_handler
