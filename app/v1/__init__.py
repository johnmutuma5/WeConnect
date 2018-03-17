from flask import Blueprint
from .storage import Storage

v1 = Blueprint ('v1', __name__)
store = Storage ()

# from . import views
from app import common_views
