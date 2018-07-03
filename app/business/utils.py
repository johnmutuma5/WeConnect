import json
from flask import jsonify
from app.business.models import Business, Review
from app.decorators import login_required
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
def register_a_business(business_data, bearer_id=None):
    # create a business to register
    try:
        business = Business.create_business(business_data, bearer_id)
    except InvalidUserInputError as error:
        # MissingDataError extends InvalidUserInputError, shall be caught too
        return jsonify({"msg": error.msg}), 401

    try:
        msg = store.add(business)
    except DuplicationError as e:
        return jsonify({"msg": e.msg}), 409
    return jsonify({
        "msg": msg['msg'],
        "id": msg['id']
        }), 201


def find_status_code(err):
    status_code = None
    if isinstance(err, DataNotFoundError):
        status_code = 404
    elif isinstance(err, PermissionDeniedError):
        status_code = 403
    elif isinstance(err, DuplicationError):
        status_code = 409
    return status_code


@login_required
def update_business_info(business_id, update_data, bearer_id=None):
    try:
        msg = store.update_business(business_id, update_data, bearer_id)
    except (DataNotFoundError, PermissionDeniedError, DuplicationError) as put_err:
        status_code = find_status_code(put_err)
        return jsonify({"msg": put_err.msg}), status_code
    return jsonify({"msg": msg}), 201


@login_required
def delete_business(business_id, bearer_id=None):
    try:
        msg = store.delete_business(business_id, bearer_id)
    except (DataNotFoundError, PermissionDeniedError) as del_err:
        status_code = find_status_code(del_err)
        return jsonify({"msg": del_err.msg}), status_code
    return jsonify({"msg": msg}), 201


@login_required
def add_a_review(business_id, review_data, bearer_id=None):
    new_review = Review.create_review(business_id, bearer_id, review_data)
    # store the review
    try:
        msg = store.add(new_review)
    except (DataNotFoundError, PermissionDeniedError) as error:
        status_code = find_status_code(error)
        return jsonify({'msg': error.msg}), status_code

    return jsonify({'msg': msg}), 201
