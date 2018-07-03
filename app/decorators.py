import jwt
import re
import json
from json.decoder import JSONDecodeError
from flask import jsonify, request, session
from jwt.exceptions import InvalidSignatureError, DecodeError
from app import config
# from functools import wraps


def wraps(original_func):
    '''
    Helps keep decorated functions with their original names in the namespace
    '''
    def decorator(original_wrapper):
        original_wrapper.__name__ = original_func.__name__
        original_wrapper.__doc__ = original_func.__doc__
        return original_wrapper
    return decorator


def handle_invalid_credentials(msg=None):
    return jsonify({
        "msg": msg or "You need to log in to perform this operation"}), 401


# Decorators
def login_required(func):
    '''
        Functions decorated with this need to accept an argument bearer_id defaulted to None
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = None
        auth = request.headers.get('Authorization')
        if not auth:
            return handle_invalid_credentials("Bearer Token authorization header missing")
        auth_pattern = r'Bearer (?P<token_string>.+\..+\..+)'
        match = re.search(auth_pattern, auth)
        if not match:
            message = None
            if not match: message = 'Invalid Token'
            return handle_invalid_credentials(message)

        access_token = match.group('token_string')
        try:
            token_payload = jwt.decode(access_token, config['SECRET_KEY'])
            bearer_id = token_payload.get('user_id')
        except (InvalidSignatureError, DecodeError):
            return handle_invalid_credentials("Invalid Token")
        return func(*args, bearer_id=bearer_id, **kwargs)
    return wrapper



def require_json(methods=['POST', 'PUT']):
    '''
        Decorates endpoints that require data, load the data from json and
        pass it to the decorated function. If a list of methods to require json
        is not passed as an argument, the decorator will enforce require
        json for POST and/or PUT as defaults. The decorated endpoint
        functions should accept a keyword argument, request_data, which should be
        defaulted to None
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.method in methods:
                return func(*args, **kwargs)

            try:
                data = json.loads(request.data.decode('utf-8'))
                # pass data to the decorated endpoint that requires json
                return func(*args, request_data=data, **kwargs)
            except JSONDecodeError:
                return jsonify({"msg": "Missing or Invalid JSON data"}), 400

        return wrapper
    return decorator
