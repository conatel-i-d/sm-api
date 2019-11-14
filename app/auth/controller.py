import json
import os
import requests


from app.api_response import Response
from flask import request, Blueprint, Response

api_description = """
Rutas de authenticacion a la API
"""

api = Blueprint('auth', __name__, url_prefix='/api/auth')


@api.route('/token_login/', methods=['POST'])
def get_token():
    body = request.get_json()
    for field in ['username', 'password']:
        if field not in body:
            return Response(json.dumps({"Error": f"El campo {field} no esta presente!"}), 400, mimetype='application/json')
    data = {
        'grant_type': 'password',
        'client_id': 'admin-cli',
        'username': body['username'],
        'password': body['password']
    }
    url = os.getenv('KEYCLOAK_URL') + 'realms/' + \
        os.getenv('REALM') + '/protocol/openid-connect/token'
    response = requests.post(url, data=data)
    if response.status_code != requests.codes.ok:
        return Response(response.text, 400, mimetype='application/json')
    tokens_data = response.json()

    result = {"access_token": tokens_data['access_token'],
              "refresh_token": tokens_data['refresh_token'], }

    return Response(json.dumps(result), 200, mimetype='application/json')


@api.route('/token_refresh/', methods=['POST'])
def refresh_token():
    body = request.get_json()
    if 'refresh_token' not in body:
        return Response(json.dumps({"Error": "El campo refresh_token no esta presente"}), 400, mimetype='application/json')
    data = {
        'grant_type': 'refresh_token',
        'client_id': 'admin-cli',
        'refresh_token': body['refresh_token'],
    }
    url = os.getenv('KEYCLOAK_URL') + 'realms/' + \
        os.getenv('REALM') + '/protocol/openid-connect/token'
    response = requests.post(url, data=data)
    data = response.json()
    if response.status_code != requests.codes.ok:
        return Response(response.text, 400, mimetype='application/json')
    result = {
        "access_token": data['access_token'],
        "refresh_token": data['refresh_token']
    }
    return Response(json.dumps(result), 200, mimetype='application/json')
