from flask import Blueprint
from .storage import DbInterface
from sqlalchemy import create_engine

v2 = Blueprint ('v2', __name__)

#import app here to avoid cyclical imports
from app import app

dbEngine = create_engine (app.config['SQLALCHEMY_DATABASE_URI'])
store = DbInterface (dbEngine)

# from . import views
from app import common_views
