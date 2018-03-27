from flask import Blueprint
from .storage import Storage
from sqlalchemy import create_engine
from config import Config

v2 = Blueprint ('v2', __name__)

dbEngine = create_engine (Config.SQLALCHEMY_DATABASE_URI)
store = Storage (dbEngine)

# from . import views
from app import common_views
