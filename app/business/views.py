import json
from flask import jsonify, request, session, Blueprint
from app.decorators import login_required, require_json
from app.helpers import inspect_data
from app.business.models import Business
from .backends import businessDbFacade as store
from ..exceptions import(InvalidUserInputError, PaginationError,
                         UnknownPropertyError)
from .utils import (get_info_response, register_a_business,
                    update_business_info, delete_business, add_a_review)


business = Blueprint('business', __name__)


@business.route('', methods=['GET', 'POST'])
@require_json
def businesses(request_data=None):
    if request.method == 'POST':
        owner = session.get('user_id')
        # this method is decorated with login required and require_json
        response = register_a_business(request_data, owner)
        return response

    businesses_info = store.get_businesses_info()
    return jsonify({"businesses": businesses_info}), 200


@business.route('/<int:business_id>', methods=['GET', 'PUT', 'DELETE'])
@require_json
def one_business(business_id, request_data=None):
    # get request issuer id
    issuer_id = session.get('user_id')

    if request.method == 'GET':
        response = get_info_response(business_id,
                                     info_type='business_data')
        return response

    elif request.method == 'PUT':
        # update_data = request.data.decode('utf-8')
        try:
            cleaned_data = inspect_data(request_data)
            # this function is decorated with login_required
            response = update_business_info(business_id, cleaned_data, issuer_id)
            return response
        except (InvalidUserInputError, UnknownPropertyError) as error:
            # MissingDataError extends InvalidUserInputError
            return jsonify({'msg': error.msg}), 422

    # handle DELETE
    response = delete_business(business_id, issuer_id)
    return response


@business.route('/search', methods=['GET'])
def search_business():
    search_params = request.args
    # expect pagnation error
    results = store.search_businesses(search_params)
    return jsonify({'results': results}), 200


@business.route('/filter', methods=['GET'])
def filter_businesses():
    filter_params = request.args
    try:
        results = store.filter_businesses(filter_params)
    except PaginationError as error:
        return jsonify({"msg": error.msg}), 422
    return jsonify({'results': results}), 200


@business.route('/<int:business_id>/reviews', methods=['GET', 'POST'])
@require_json
def reviews(business_id, request_data=None):
    # business_id = Business.gen_id_string (business_id)
    if request.method == 'GET':
        response = get_info_response(business_id, 'business_reviews')
        return response

    review_data = json.loads(request.data.decode('utf-8'))
    # get logged in user
    author_id = session.get('user_id')
    response = add_a_review(business_id, review_data)
    return response
