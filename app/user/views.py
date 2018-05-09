import json, jwt, re
from flask import jsonify, request, session, url_for, Blueprint

from app import config
from .backends import userDbFacade as store
from .models import User, PasswordResetToken
from ..helpers import generate_token, inspect_data, verify_password
from app.decorators import login_required, require_json
from ..exceptions import (DuplicationError, DataNotFoundError,
                         PermissionDeniedError, InvalidUserInputError)

'''
BEGINNING OF ENDOPOINTS
'''

user = Blueprint("user", __name__)


@user.route('/register', methods=['POST'])
@require_json
def register():
    data = json.loads(request.data.decode('utf-8'))

    try:
        user = User.create_user(data)
    except InvalidUserInputError as e:
        return jsonify({"msg": e.msg})

    try:
        msg = store.add(user)
    except DuplicationError as e:
        return jsonify({'msg': e.msg}), 401

    return jsonify({"msg": msg}), 200


@user.route('/login', methods=['POST'])
@require_json
def login():
    login_data = json.loads(request.data.decode('utf-8'))
    username = login_data['username']

    target_user = store.get_user(username)
    if target_user:
        password = login_data['password']
        passhash = target_user.password
        password_match = verify_password(password, passhash)

    if not target_user or not password_match:
        return jsonify({"msg": "Invalid username or password"}), 401

    session['user_id'] = target_user.id
    secret = config['SECRET_KEY']
    msg = "Logged in {}".format(username)
    access_token = jwt.encode({'user_id': target_user.id}, secret)
    access_token = access_token.decode('utf-8')
    return jsonify({'msg': msg, 'access_token': access_token}), 200


@user.route('/logout', methods=['POST'])
@login_required
def logout():
    session.pop('user_id')
    return jsonify({"msg": "Logged out successfully!"}), 200


@user.route('/reset-password', methods=['POST'])
@require_json
def reset_password():
    username = (json.loads(request.data.decode('utf-8'))).get('username')
    # user initiates request with their username
    if username:
        target_user = store.get_user(username)
        if target_user:
            token_string = generate_token()
            token_obj = PasswordResetToken(token_string, username)
            store.add_token(token_obj, username)
            reset_link = url_for('.update_password', _external=True, t=token_string)
            # to email reset_link with token url parameter to user's email address
            return jsonify({"reset_link": reset_link}), 200  # for testing
        return jsonify({"msg": "Invalid Username"}), 404
    return jsonify({"msg": "Please supply your username"}), 401


@user.route('/reset-password/verify', methods=['POST', 'GET'])
@require_json
def update_password():
    if request.method == 'GET':
        return jsonify({'msg': 'Please supply your new password'})

    url_query_token = request.args.get('t')
    new_password = (json.loads(request.data.decode('utf-8')))\
        .get('new_password')
    if url_query_token:
        token_obj, token_bearer = store.get_token_tuple(url_query_token)
        if token_obj:
            if not token_obj.expired:
                store.update_user_password(token_bearer, new_password)
                # ensure tokens are one time use
                store.destroy_token(token_obj)
                return jsonify({"msg": "Password updated successfully"})
            # destroy token if expired
            store.destroy_token(token_obj)
            return jsonify({'msg': 'Token expired'})
    return jsonify({"msg": "Invalid token"}), 401
