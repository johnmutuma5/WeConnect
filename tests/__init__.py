import unittest
import json, requests
from .dummies import user_data


requests = requests.Session() #persist cookies across requests

class BaseAPITestSetUp (unittest.TestCase):
    def setUp (self):
        self.base_url = 'http://0.0.0.0:8080'
        self.headers = {'content-type': 'application/json'}
        self.register_user (user_data)


class TestHelpers ():
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
