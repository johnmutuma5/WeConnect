from . import v2, store
from app import config
from .models import User, Business, Review, Token
from ..helpers import generate_token
from flask import jsonify, request, session, url_for
from ..exceptions import (DuplicationError, DataNotFoundError,
                         PermissionDeniedError, InvalidUserInputError)
import json, jwt, re
from jwt.exceptions import InvalidSignatureError, DecodeError


'''
DECORATE FUNCTIONALITIES THAT REQUIRE ACTIVE SESSIONS
'''
def handle_invalid_credentials():
    return jsonify({
        "msg": "You need to log in to perform this operation"
    }), 401


def login_required(func):
    def wrapper(*args, **kwargs):
        access_token = None
        auth = request.headers.get('Authorization')
        auth_pattern = r'Bearer (?P<token_string>.+\..+\..+)'
        match = re.search(auth_pattern, auth)
        if match:
            access_token = match.group('token_string')
            try:
                token_payload = jwt.decode(access_token, config['SECRET_KEY'])
                bearer_id = token_payload.get('user_id')
                session['user_id'] = bearer_id
            except (InvalidSignatureError, DecodeError):
                return handle_invalid_credentials()
            return func(*args, **kwargs)
        return handle_invalid_credentials()


    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


@login_required
def register_a_business(business_data):
    # create a business to register
    owner = session.get('user_id')
    try:
        business = Business.create_business(business_data, owner)
    except InvalidUserInputError as e:
        # MissingDataError extends InvalidUserInputError
        return jsonify({"msg": e.msg})

    try:
        msg = store.add(business)
    except DuplicationError as e:
        return jsonify({"msg": e.msg}), 401

    return jsonify({"msg": msg}), 201


def find_status_code (err):
    status_code = None
    if type (err) == DataNotFoundError:
        status_code = 404
    elif type(err) == PermissionDeniedError:
        status_code = 403
    elif type(err) == DuplicationError:
        status_code = 409
    elif type(err) == InvalidUserInputError:
        status_code = 422
    return status_code


@login_required
def update_business_info(business_id, update_data):
    issuer_id = session.get('user_id')
    try:
        msg = store.update_business(business_id, update_data, issuer_id)
    except (DataNotFoundError, PermissionDeniedError, DuplicationError) as put_err:
        status_code = find_status_code(put_err)
        return jsonify({"msg": put_err.msg}), status_code
    return jsonify({"msg": msg}), 201


@login_required
def delete_business(business_id):
    issuer_id = session.get('user_id')
    try:
        msg = store.delete_business(business_id, issuer_id)
    except (DataNotFoundError, PermissionDeniedError) as del_err:
        status_code = find_status_code(del_err)
        return jsonify({"msg": del_err.msg}), status_code
    return jsonify({"msg": msg}), 201


@login_required
def add_a_review(business_id, review_data):
    author_id = session.get('user_id')
    new_review = Review.create_review(business_id, author_id, review_data)
    # store the review
    msg = store.add(new_review)
    return jsonify({'msg': msg}), 200


def get_info_response(business_id, info_type):
    '''
        Loads GET info of a single business i.e. reviews, or the business's info
    '''
    _call = {
        "business_data": store.get_business_info,
        "business_reviews": store.get_reviews_info
    }[info_type]

    try:
        info = _call(business_id)
    except DataNotFoundError as err:
        # if need be, we can log e.expression here
        return jsonify({"msg": err.msg}), 404
    return jsonify({"info": info}), 200


'''
BEGINNING OF ENDOPOINTS
'''


@v2.route('/auth/register', methods=['POST'])
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


@v2.route('/auth/login', methods=['POST'])
def login():
    login_data = json.loads(request.data.decode('utf-8'))
    username = login_data['username']

    target_user = store.get_user(username)
    if target_user:
        no_password_match = not target_user.password == login_data['password']

    if not target_user or no_password_match:
        return jsonify({"msg": "Invalid username or password"}), 401

    session['user_id'] = target_user.id
    secret = config['SECRET_KEY']
    msg = "Logged in {}".format(username)
    access_token = jwt.encode({'user_id': target_user.id}, secret)
    access_token = access_token.decode('utf-8')
    return jsonify({'msg': msg, 'access_token': access_token}), 200


@v2.route('/auth/logout', methods=['POST'])
@login_required
def logout():
    session.pop('user_id')
    return jsonify({"msg": "Logged out successfully!"}), 200


@v2.route('/businesses', methods=['GET', 'POST'])
def businesses():
    if request.method == 'POST':
        business_data = json.loads(request.data.decode('utf-8'))
        owner = session.get('user_id')
        # this method is decorated with login required
        response = register_a_business(business_data)
        return response

    businesses_info = store.get_businesses_info()
    return jsonify({"businesses": businesses_info}), 200


@v2.route('/businesses/<int:business_id>',
          methods=['GET', 'PUT', 'DELETE'])
def business(business_id):
    if request.method == 'GET':
        response = get_info_response(business_id, info_type='business_data')
        return response

    elif request.method == 'PUT':
        update_data = json.loads(request.data.decode('utf-8'))
        # this method is decorated with login_required
        response = update_business_info(business_id, update_data)
        return response

    # handle DELETE
    response = delete_business(business_id)
    return response


@v2.route('/businesses/search', methods=['GET'])
def search_business():
    search_key = request.args.get('q')
    results = store.search_businesses(search_key)
    return jsonify({'results': results})


@v2.route('/businesses/<int:business_id>/reviews',
          methods=['GET', 'POST'])
def reviews(business_id):
    # business_id = Business.gen_id_string (business_id)
    if request.method == 'GET':
        response = get_info_response(business_id, 'business_reviews')
        return response

    review_data = json.loads(request.data.decode('utf-8'))
    # get logged in user
    author_id = session.get('user_id')
    response = add_a_review(business_id, review_data)
    return response


@v2.route('/auth/reset-password', methods=['POST'])
def reset_password():
    username = (json.loads(request.data.decode('utf-8'))).get('username')
    # user initiates request with their username
    if username:
        target_user = store.get_user(username)
        if target_user:
            token_string = generate_token()
            token_obj = Token(token_string, username)
            store.add_token(token_obj, username)
            reset_link = url_for('.update_password', _external=True, t=token_string)
            # to email reset_link with token url parameter to user's email address
            return jsonify({"reset_link": reset_link}), 200  # for testing
        return jsonify({"msg": "Invalid Username"}), 404
    return jsonify({"msg": "Please supply your username"}), 401


@v2.route('/auth/reset-password/verify', methods=['POST', 'GET'])
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
