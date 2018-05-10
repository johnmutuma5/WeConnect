import json
from flask import jsonify, request, session, Blueprint
from app.decorators import login_required, require_json
from app.business.models import Business
from .backends import businessDbFacade as store
from ..exceptions import InvalidUserInputError
from .utils import (get_info_response, register_a_business,
    update_business_info, delete_business, add_a_review)


business = Blueprint('business', __name__)


@business.route('', methods=['GET', 'POST'])
@require_json
def businesses():
    if request.method == 'POST':
        business_data = request.data.decode('utf-8')
        owner = session.get('user_id')
        # this method is decorated with login required and require_json
        response = register_a_business(business_data)
        return response

    businesses_info = store.get_businesses_info()
    return jsonify({"businesses": businesses_info}), 200


@business.route('/<int:business_id>', methods=['GET', 'PUT', 'DELETE'])
@require_json
def one_business(business_id):
    if request.method == 'GET':
        response = get_info_response(business_id, info_type='business_data')
        return response

    elif request.method == 'PUT':
        update_data = request.data.decode('utf-8')
        try:
            # this method is decorated with login_required and require_json
            response = update_business_info(business_id, update_data)
            return response
        except InvalidUserInputError as e:
            # MissingDataError extends InvalidUserInputError
            return jsonify({'msg': e.msg}), 422


    # handle DELETE
    response = delete_business(business_id)
    return response


@business.route('/search', methods=['GET'])
def search_business():
    search_key = request.args.get('q')
    results = store.search_businesses(search_key)
    return jsonify({'results': results})


@business.route('/filter', methods=['GET'])
def filter_businesses():
    filter_params = request.args
    try:
        results = store.filter_businesses(filter_params)
    except PaginationError as error:
        return jsonify({"msg": error.msg})
    return jsonify({'results': results})


@business.route('/<int:business_id>/reviews', methods=['GET', 'POST'])
@require_json
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
