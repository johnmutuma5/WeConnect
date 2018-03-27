from flask import Blueprint
from .storage import Storage
from sqlalchemy import create_engine

v2 = Blueprint ('v2', __name__)

#import app here to avoid cyclical imports
from app import app

dbEngine = create_engine (app.config['SQLALCHEMY_DATABASE_URI'])
store = Storage (dbEngine)

# from . import views
from app import common_views
