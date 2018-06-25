from app.user import auth_urls_blueprint as auth, views

# auth url prefix = '/api/v2/auth'
auth.add_url_rule(rule='/register',
                  view_func=views.register,
                  methods=['POST'])
auth.add_url_rule(rule='/login',
                  view_func=views.login,
                  methods=['POST'])
auth.add_url_rule(rule='/personal-profile',
                  view_func=views.user_private_profile,
                  methods=['GET'])
auth.add_url_rule(rule='/logout',
                  view_func=views.logout,
                  methods=['POST'])
auth.add_url_rule(rule='/reset-password',
                  view_func=views.initiate_password_reset,
                  methods=['POST'])
auth.add_url_rule(rule='/reset-password/verify',
                  view_func=views.complete_password_reset,
                  methods=['POST', 'GET'])
