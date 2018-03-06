from app import app, store
from .models import User, Business, Review
from flask import jsonify, request
import json

@app.route('/api/v1/auth/register', methods = ['POST'])
def register ():
    data = json.loads(request.data.decode('utf-8'))
    user = User.create_user (data)

    msg = store.add_user (user)
    return jsonify (msg), 200
