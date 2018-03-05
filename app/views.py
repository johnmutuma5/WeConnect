from app import app
from flask import jsonify

@app.route('/api/auth/register', methods = ['POST'])
def register ():
    return jsonify ('connected')
