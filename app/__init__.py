from flask import Flask

app = Flask (__name__)
app.config.from_object ('config.DevelopmentConfig')

# Blueprints
# from .v1 import v1
from .v2 import v2

# app.register_blueprint (v1, url_prefix = "/api/v1")
app.register_blueprint (v2, url_prefix = "/api/v2")
