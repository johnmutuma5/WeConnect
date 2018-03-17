from flask import Flask

# Blueprints
from .v1 import v1

app = Flask (__name__)
app.config.from_object ('config.Config')

app.register_blueprint (v1, url_prefix = "/api/v1")
