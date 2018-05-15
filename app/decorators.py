import jwt
import re
from flask import jsonify, request, session
from jwt.exceptions import InvalidSignatureError, DecodeError
from app import config
from functools import wraps


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
    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = None
        auth = request.headers.get('Authorization')
        if not auth:
            return handle_invalid_credentials("Bearer Token authorization header missing")
        auth_pattern = r'Bearer (?P<token_string>.+\..+\..+)'
        match = re.search(auth_pattern, auth)

        if not match or not session.get('user_id'):
            message = None
            if not match: message = 'Invalid Token'
            return handle_invalid_credentials(message)

        access_token = match.group('token_string')
        try:
            token_payload = jwt.decode(access_token, config['SECRET_KEY'])
            bearer_id = token_payload.get('user_id')
            session['user_id'] = bearer_id
        except (InvalidSignatureError, DecodeError):
            return handle_invalid_credentials("Invalid Token")
        return func(*args, **kwargs)
    return wrapper


def require_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method in ['POST',
                              'PUT'] and not request.data.decode('utf-8'):
            return jsonify({"msg": "Could not handle the request"}), 401

        return func(*args, **kwargs)
    return wrapper
