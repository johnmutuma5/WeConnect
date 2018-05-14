import unittest
import json
import re
from app.tests import BaseAPITestSetUp
from app.tests.dummies import(user_data, invalid_credentials, login_data,
                              business_data)


class TestGetUserProfileCase (BaseAPITestSetUp):

    def test_generates_user_profile(self):
        res = self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.register_business(business_data, access_token)

        # profile url
        url = self.base_url + '/api/v2/auth/personal-profile'
        headers={
            **self.headers,
            'authorization': 'Bearer {}'.format(access_token)
        }
        response = self.app.get(url, headers=headers)
        data = json.loads(response.data.decode('utf-8'))
        profile = data['profile']
        user_businesses = profile['businesses']
        username = profile['username']
        self.assertTrue(user_businesses[0]['name'] == business_data['name'])
        self.assertTrue(username == user_data['username'])



if __name__ == "__main__":
    unittest.main(module=__name__)
