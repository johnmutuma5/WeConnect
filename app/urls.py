from app import app, index
from app.business.urls import business as business_urls_blueprint
from app.user.urls import auth as auth_urls_blueprint

app.add_url_rule(rule='/',
                 view_func=index.index,
                 methods=['GET'])
app.add_url_rule(rule='/api/documentation',
                 view_func=index.documentation,
                 methods=['GET'])
# more url rules from blueprints
app.register_blueprint(blueprint=business_urls_blueprint,
                       url_prefix="/api/v2/businesses")
app.register_blueprint(blueprint=auth_urls_blueprint,
                       url_prefix="/api/v2/auth")
