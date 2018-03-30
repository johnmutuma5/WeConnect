import unittest
import json
from .dummies import login_data
from app import app
from app.v2.models import Base
from app.v2 import dbEngine


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
        # res = requests.post(url, data = json.dumps(user_data), headers = self.headers)
        res = self.app.post(url, data=json.dumps(
            user_data), headers=self.headers)
        return res

    def login_user(self, login_data):
        url = self.base_url + '/api/v2/auth/login'
        res = self.app.post(url, data=json.dumps(
            login_data), headers=self.headers)
        return res
    #

    def logout_user(self):
        url = self.base_url + '/api/v2/auth/logout'
        return self.app.post(url)
    #

    def register_business(self, bizdata):
        self.login_user(login_data)
        url = self.base_url + '/api/v2/businesses'
        return self.app.post(url, data=json.dumps(bizdata), headers=self.headers)
    #

    def get_businesses(self):
        url = self.base_url + '/api/v2/businesses'
        return self.app.get(url)
    #

    def get_business(self, raw_id):
        url = self.base_url + '/api/v2/businesses/{id:}'.format(id=raw_id)
        return self.app.get(url)
    #

    def update_business(self, raw_id, update_data):
        url = self.base_url + '/api/v2/businesses/{id:}'.format(id=raw_id)
        return self.app.put(url, data=json.dumps(update_data), headers=self.headers)
    #

    def delete_business(self, raw_id):
        url = self.base_url + '/api/v2/businesses/{id:}'.format(id=raw_id)
        return self.app.delete(url)
    #

    def make_review(self, raw_id, review_data):
        url = self.base_url + \
            '/api/v2/businesses/{id:}/reviews'.format(id=raw_id)
        return self.app.post(url, data=json.dumps(review_data), headers=self.headers)
    #

    def get_all_reviews(self, raw_id):
        url = self.base_url + \
            '/api/v2/businesses/{id:}/reviews'.format(id=raw_id)
        return self.app.get(url)

    def reset_password(self, reset_data, token=None):
        if token:
            url = self.base_url + \
                '/api/v2/auth/reset-password?t={}'.format(token)
        else:
            url = self.base_url + '/api/v2/auth/reset-password'
        return self.app.post(url, data=json.dumps(reset_data), headers=self.headers)


class BaseAPITestSetUp (unittest.TestCase):
    def setUp(self):
        self.testHelper = TestHelper()
        Base.metadata.create_all(dbEngine)

    def tearDown(self):
        Base.metadata.drop_all(dbEngine)
