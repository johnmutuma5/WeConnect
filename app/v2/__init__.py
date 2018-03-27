from flask import Blueprint
from .storage import Storage

v2 = Blueprint ('v2', __name__)
store = Storage ()

# from . import views
from app import common_views
