'''
Flask wsgi application
'''

from flask import Flask

app = Flask(__name__)
app.config.from_object('config.env')
config = app.config

from app import urls
