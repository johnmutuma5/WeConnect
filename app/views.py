from app import app, store
from .models import User, Business, Review
from flask import jsonify, request, session
import json



@app.route('/api/v1/auth/register', methods = ['POST'])
def register ():
    data = json.loads(request.data.decode('utf-8'))
    user = User.create_user (data)

    msg = store.add_user (user)
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
        msg = "logged in {} successfully".format(username)
        return jsonify(msg), 200
