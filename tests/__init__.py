import unittest
import json, requests
from .dummies import user_data, login_data


requests = requests.Session() #persist cookies across requests

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
        self.login_user (login_data)
        url = self.base_url + '/api/v1/businesses'
        return requests.post(url, data = json.dumps(bizdata), headers = self.headers)

    def get_businesses (self):
        url = self.base_url + '/api/v1/businesses'
        return requests.get(url)

    def get_business (self, raw_id):
        url = self.base_url + '/api/v1/businesses/{id:}'.format(id = raw_id)
        return requests.get(url)

    def update_business (self, raw_id, update_data):
        url = self.base_url + '/api/v1/businesses/{id:}'.format(id = raw_id)
        return requests.put (url, data = json.dumps(update_data))

    def delete_business (self, raw_id):
        url = self.base_url + '/api/v1/businesses/{id:}'.format(id = raw_id)
        return requests.delete (url)


class BaseAPITestSetUp (unittest.TestCase):
    def setUp (self):
        self.testHelper = TestHelper ()
