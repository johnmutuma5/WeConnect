from app.business import views, business_urls_blueprint as business

# business url prefix = '/api/v2/busineneses'
business.add_url_rule(rule='',
                      view_func=views.businesses,
                      methods=['GET', 'POST'])
business.add_url_rule(rule='/<int:business_id>',
                      view_func=views.one_business,
                      methods=['GET', 'PUT', 'DELETE'])
business.add_url_rule(rule='/search',
                      view_func=views.search_business,
                      methods=['GET'])
business.add_url_rule(rule='/filter',
                      view_func=views.filter_businesses,
                      methods=['GET'])
business.add_url_rule(rule='/<int:business_id>/reviews',
                      view_func=views.reviews,
                      methods=['GET', 'POST'])
