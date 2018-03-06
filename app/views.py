from app import app, store
from .models import User, Business, Review
from flask import jsonify, request, session
from .exceptions import DuplicationError
import json


@app.route('/api/v1/auth/register', methods = ['POST'])
def register ():
    data = json.loads(request.data.decode('utf-8'))
    user = User.create_user (data)

    try:
        msg = store.add_user (user)
    except DuplicationError as e:
        return jsonify({'msg': e.msg}), 401

    return jsonify (msg), 200


@app.route ('/api/v1/auth/login', methods = ['POST'])
def login ():
    login_data = json.loads(request.data.decode('utf-8'))
    username = login_data['username']

    target_user = store.users.get(username)

    if not target_user:
        return jsonify ('Could not login'), 401

    if target_user.password == login_data['password']:
        session['user'] = username
        msg = "logged in {}".format(username)
        return jsonify({'msg': msg}), 200


@app.route ('/api/v1/auth/logout', methods = ['POST'])
def logout ():
    if session.get('user'):
        return jsonify({"msg": "logged out successfully!"}), 200

    return jsonify({"msg": "unsuccessfully!"}), 500
