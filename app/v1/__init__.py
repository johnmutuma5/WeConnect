from flask import Flask
from .storage import Storage

app = Flask (__name__)
app.config.from_object ('config.Config')
store = Storage ()

from app.v1 import views
