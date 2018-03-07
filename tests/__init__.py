import unittest
import json, requests
from .dummies import user_data
from app import store


requests = requests.Session() #persist cookies across requests

class TestHelper ():
    '''
        methods:
            login_user
                params: login_data
            register_user:
                params: user_data
            logout_user:
                params: None
            register_business:
                params: bizdata
    '''

    def __init__ (self):
        self.base_url = 'http://0.0.0.0:8080'
        self.headers = {'content-type': 'application/json'}

    def register_user (self, user_data):
        url = self.base_url + '/api/v1/auth/register'
        res = requests.post(url, data = json.dumps(user_data), headers = self.headers)
        return res

    def login_user (self, login_data):
        url = self.base_url + '/api/v1/auth/login'
        res = requests.post(url, data = json.dumps(login_data), headers = self.headers)
        return res

    def logout_user (self):
        url = self.base_url + '/api/v1/auth/logout'
        return requests.post(url)

    def register_business (self, bizdata):
        url = self.base_url + '/api/v1/businesses'
        return requests.post(url, data = json.dumps(bizdata), headers = self.headers)

    def get_businesses (self):
        url = self.base_url + '/api/v1/businesses'
        return requests.get(url)


class BaseAPITestSetUp (unittest.TestCase):
    def setUp (self):
        self.testHelper = TestHelper ()

    @classmethod
    def tearDownClass (cls):
        store.clear ()
