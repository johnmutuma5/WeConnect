import json
import jwt
from flask import jsonify, request, session, url_for
from app import config
from app.decorators import login_required, require_json
from app.mailing.mailer import Mailer
from .backends import userDbFacade as store
from .models import User, PasswordResetToken
from ..helpers import generate_token, verify_password
from ..exceptions import DuplicationError, InvalidUserInputError

'''
BEGINNING OF ENDOPOINTS
'''


@require_json(methods=['POST'])
def register(request_data=None):
    data = request_data

    try:
        new_user = User.create_user(data)
    except InvalidUserInputError as e:
        return jsonify({"msg": e.msg}), 422

    try:
        msg = store.add(new_user)
    except DuplicationError as e:
        return jsonify({'msg': e.msg}), 409

    return jsonify({"msg": msg}), 201


@require_json(methods=['POST'])
def login(request_data=None):
    login_data = request_data
    username = login_data['username']

    target_user = store.get_user(username, column='username')
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
    return jsonify({'msg': msg, 'access_token': access_token, 'id': target_user.id}), 200


@login_required
def user_private_profile(bearer_id=None):
    profile_type = 'private'
    target_user = store.get_user(bearer_id, column='id')
    profile = store.fetch_user_profile(target_user, profile_type='private')
    return jsonify({"profile": profile}), 200



@login_required
def logout(bearer_id=None):
    # session.pop('user_id')
    return jsonify({"msg": "Logged out successfully!"}), 200


@require_json(methods=['POST'])
def initiate_password_reset(request_data=None):
    # user initiates request with their username
    username = request_data.get('username')
    if not username:
        return jsonify({"msg": "Please supply your username"}), 401

    target_user = store.get_user(username, column='username')
    if not target_user:
        return jsonify({"msg": "Invalid Username"}), 404

    token_string = generate_token()
    reset_link = url_for('.complete_password_reset', _external=True,
                         t=token_string)
    # email reset_link with token url parameter to user's email address
    mailer = Mailer()
    recipient = target_user.email
    mailer.send_reset_link(reset_link, recipient)
    token_obj = PasswordResetToken(token_string, username)
    store.add_token(token_obj, username)
    return jsonify({"reset_link": reset_link}), 200  # for testing


@require_json(methods=['POST'])
def complete_password_reset(request_data=None):
    if request.method == 'GET':
        return jsonify({'msg': 'Please supply your new password'})

    url_query_token = request.args.get('t')
    new_password = request_data.get('new_password')
    if not url_query_token:
        return jsonify({"msg": "Password reset token is missing"})

    # fetch the token object and the bearer
    token_obj, token_bearer = store.get_token_tuple(url_query_token)
    if not token_obj:
        return jsonify({"msg": "Invalid token"}), 401

    if token_obj.expired:
        # destroy expired token
        store.destroy_token(token_obj)
        return jsonify({'msg': 'Token expired'}), 401
    # at this point on this should be an eligible reset
    try:
        store.update_user_password(token_bearer, new_password)
        # ensure tokens are one time use
        store.destroy_token(token_obj)
    except InvalidUserInputError as error: # check min password length
        return jsonify({"msg": error.msg}), 422
    return jsonify({"msg": "Password updated successfully"}), 201
