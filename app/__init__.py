from flask import Flask

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
config = app.config

# fetch Blueprints
from app.business.views import business
from app.user.views import user

app.register_blueprint(business, url_prefix="/api/v2/businesses")
app.register_blueprint(user, url_prefix="/api/v2/auth")
