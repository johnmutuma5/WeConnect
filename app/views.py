from app import app, store
from .models import User, Business, Review
from flask import jsonify, request, session
from .exceptions import (DuplicationError, DataNotFoundError,
                            PermissionDeniedError, InvalidUserInputError)
import json


''''''
# DECORATE FUNCTIONALITIES THAT REQUIRE ACTIVE SESSIONS
''''''

def login_required (func):
    def wrapper (*args, **kwargs):
        logged_user = session.get('user_id')
        if logged_user:
            return func (*args, **kwargs)
        return jsonify ({"msg": "You need to log in to perform this operation"}), 401

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper

@login_required
def register_a_business (business_data, owner):
    # create a business to register
    business = Business.create_business (business_data, owner)
    try:
        msg = store.add (business)
    except DuplicationError as e:
        business.handback_unused_id () # class Business auto generates ids
        return jsonify ({"msg": e.msg}), 401

    return jsonify({"msg": msg}), 201


def find_status_code (err):
    if type (err) == DataNotFoundError:
        status_code = 404
    else:
        status_code = 401
    return status_code


@login_required
def update_business_info (business_id, update_data, issuer_id):
    try:
        msg = store.update_business (business_id, update_data, issuer_id)
    except (DataNotFoundError, PermissionDeniedError, DuplicationError) as put_err:
        status_code = find_status_code (put_err)
        return jsonify({"msg": put_err.msg}), status_code
    return jsonify({"msg": msg}), 201


@login_required
def delete_business (business_id, issuer_id):
    try:
        msg = store.delete_business (business_id, issuer_id)
    except (DataNotFoundError, PermissionDeniedError) as del_err:
        status_code = find_status_code (del_err)
        return jsonify({"msg": del_err.msg}), status_code
    return jsonify({"msg": msg}), 201


@login_required
def add_a_review (business_id, author_id, review_data):
    new_review = Review.create_review (business_id, author_id, review_data)
    # store the review
    msg = store.add_review (new_review)
    return jsonify ({'msg': msg}), 200



def get_info_response (business_id, info_type):
    '''
        Loads GET info of a single business i.e. reviews, or the business's info
    '''
    _call = {
        "business_data": store.get_business_info,
        "business_reviews": store.get_reviews_info
    }[info_type]

    try:
        info =  _call (business_id)
    except DataNotFoundError as err:
        # if need be, we can log e.expression here
        return jsonify ({"msg": err.msg}), 404
    return jsonify ({"info": info}), 200



''''''
# BEGINNING OF ENDOPOINTS
''''''

@app.route('/api/v1/auth/register', methods = ['POST'])
def register ():
    data = json.loads(request.data.decode('utf-8'))

    try:
        user = User.create_user (data)
    except InvalidUserInputError as e:
        return jsonify ({"msg": e.msg})

    try:
        msg = store.add (user)
    except DuplicationError as e:
        # user.handback_unused_id ()
        return jsonify({'msg': e.msg}), 401

    return jsonify ({"msg": msg}), 200


@app.route ('/api/v1/auth/login', methods = ['POST'])
def login ():
    login_data = json.loads(request.data.decode('utf-8'))
    username = login_data['username']

    target_user = store.users.get(username)
    if target_user:
        no_password_match = not target_user.password == login_data['password']

    if not target_user or no_password_match:
        return jsonify ({"msg": "Invalid username or password"}), 401

    session['user_id'] = target_user.id
    msg = "Logged in {}".format(username)
    return jsonify({'msg': msg}), 200


@app.route ('/api/v1/auth/logout', methods = ['POST'])
@login_required
def logout ():
    session.pop('user_id')
    return jsonify({"msg": "Logged out successfully!"}), 200

@app.route ('/api/v1/businesses', methods = ['GET', 'POST'])
def businesses ():
    if request.method == 'POST':
        business_data = json.loads (request.data.decode('utf-8'))
        owner = session.get ('user_id')
        response = register_a_business (business_data, owner) # this method is decorated with login required
        return response

    businesses_info = store.get_businesses_info ()
    return jsonify ({"businesses": businesses_info}), 200



@app.route ('/api/v1/businesses/<int:business_id>', methods = ['GET', 'PUT', 'DELETE'])
def business (business_id):
    business_id = Business.gen_id_string (business_id)
    issuer_id = session.get ('user_id')
    if request.method == 'GET':
        response = get_info_response (business_id, info_type = 'business_data')
        return response

    elif request.method == 'PUT':
        update_data = json.loads (request.data.decode('utf-8'))
        response = update_business_info (business_id, update_data, issuer_id) # this method is decorated with login_required
        return response

    # handle DELETE
    response = delete_business (business_id, issuer_id)
    return response



@app.route ('/api/v1/businesses/<int:business_id>/reviews', methods = ['GET', 'POST'])
def reviews (business_id):
    business_id = Business.gen_id_string (business_id)
    if request.method == 'GET':
        response = get_info_response (business_id, 'business_reviews')
        return response

    review_data = json.loads(request.data.decode ('utf-8'))
    # get logged in user
    author_id = session.get ('user_id')
    response = add_a_review (business_id, author_id, review_data)
    return response


@app.route ('/api/v1/auth/reset-password', methods = ['POST'])
def reset_password ():
    return jsonify ({"msg": "Under construction"}), 501
