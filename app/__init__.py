'''
Flask wsgi application
'''

from flask import Flask
from .CORS_Middleware.middleware import CORSMiddleware

app = Flask(__name__)
app = CORSMiddleware(app)
app.config.from_object('config.env')
config = app.config

from app import urls
