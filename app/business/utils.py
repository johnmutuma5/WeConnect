import json
from flask import jsonify, session
from app.business.models import Business, Review
from app.decorators import login_required
from app.helpers import inspect_data
from .backends import businessDbFacade as store
from ..exceptions import (DuplicationError, DataNotFoundError,
                         PermissionDeniedError, InvalidUserInputError)


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


@login_required
def register_a_business(business_json):
    # create a business to register
    owner = session.get('user_id')
    try:
        business_data = json.loads(business_json)
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
    return status_code


@login_required
def update_business_info(business_id, update_json):
    issuer_id = session.get('user_id')
    try:
        update_data = json.loads(update_json)
        cleaned_data = inspect_data(update_data)

        msg = store.update_business(business_id, cleaned_data, issuer_id)
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
