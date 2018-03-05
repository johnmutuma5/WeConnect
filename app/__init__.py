from .entities import User, Business, Review
from flask import Flask

app = Flask (__name__)
app.config.from_object ('config.Config')

from app import views
