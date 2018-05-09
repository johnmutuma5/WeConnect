import unittest
import json
from .dummies import login_data
from app import app
from app.storage.base import init_db, drop_tables
from app.business.backends import businessDbFacade
from app.user.backends import userDbFacade


# requests = requests.Session() #persist cookies across requests

class TestHelper ():
    '''
        methods:
            login_user
                params: dict::login_data
            register_user:
                params: dict::user_data
            logout_user:
                params: None
            register_business:
                params: dict::bizdata
            get_businesses:
                params: None
            get_business:
                params: int::raw_id
    '''

    def __init__(self):
        self.base_url = 'http://127.0.0.1:8080'
        self.headers = {'content-type': 'application/json'}
        self.app = app.test_client()

    def register_user(self, user_data):
        url = self.base_url + '/api/v2/auth/register'
        res = self.app.post(url, data=json.dumps(
            user_data), headers=self.headers)
        return res

    def login_user(self, login_data):
        url = self.base_url + '/api/v2/auth/login'
        res = self.app.post(url, data=json.dumps(
            login_data), headers=self.headers)
        return res
    #

    def logout_user(self, token=None):
        url = self.base_url + '/api/v2/auth/logout'
        return self.app.post(url,
            headers={**self.headers, 'authorization': 'Bearer {}'.format(token)})
    #

    def register_business(self, bizdata, token=None):
        url = self.base_url + '/api/v2/businesses'
        return self.app.post(url, data=json.dumps(bizdata),
            headers={**self.headers, 'authorization': 'Bearer {}'.format(token)})
    #

    def get_businesses(self):
        url = self.base_url + '/api/v2/businesses'
        return self.app.get(url)
    #

    def get_business(self, raw_id):
        url = self.base_url + '/api/v2/businesses/{id:}'.format(id=raw_id)
        return self.app.get(url)
    #
    def search_business(self, search_key):
        url = self.base_url + '/api/v2/businesses/search'
        return self.app.get(url, query_string={'q': search_key})

    def update_business(self, raw_id, update_data, token=None):
        url = self.base_url + '/api/v2/businesses/{id:}'.format(id=raw_id)
        return self.app.put(url, data=json.dumps(update_data),
            headers={**self.headers, 'authorization': 'Bearer {}'.format(token)})
    #

    def delete_business(self, raw_id, token=None):
        url = self.base_url + '/api/v2/businesses/{id:}'.format(id=raw_id)
        return self.app.delete(url,
            headers={**self.headers, 'authorization': 'Bearer {}'.format(token)})
    #

    def make_review(self, raw_id, review_data, token=None):
        url = self.base_url + \
            '/api/v2/businesses/{id:}/reviews'.format(id=raw_id)
        return self.app.post(url, data=json.dumps(review_data),
            headers={**self.headers, 'authorization': 'Bearer {}'.format(token)})
    #

    def get_all_reviews(self, raw_id):
        url = self.base_url + \
            '/api/v2/businesses/{id:}/reviews'.format(id=raw_id)
        return self.app.get(url)

    def reset_password(self, reset_data, token=None):
        url = self.base_url + '/api/v2/auth/reset-password'
        return self.app.post(url, data=json.dumps(reset_data), headers=self.headers)

    def reset_password_verify(self, reset_link, method=None, reset_data=None):
        url = reset_link
        if not method:
            return self.app.get(url)
        return self.app.post(url, data=json.dumps(reset_data), headers=self.headers)

class BaseAPITestSetUp (unittest.TestCase):
    def setUp(self):
        self.testHelper = TestHelper()
        init_db()

    def tearDown(self):
        drop_tables()
