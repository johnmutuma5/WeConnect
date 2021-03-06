import unittest
import json
import re
from app.tests import BaseAPITestSetUp
from app.tests.dummies import user_data, invalid_credentials, login_data


class TestUserCase (BaseAPITestSetUp):

    def test_user_can_login(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        msg = (json.loads(res.data.decode("utf-8")))['msg']

        pattern = r"Logged in (?P<username>.+)"
        self.assertRegexpMatches(msg, pattern)
        # extract username from regular expression
        match = re.search(pattern, msg)
        logged_user = match.group('username')
        self.assertEqual(login_data['username'], logged_user)


    def test_validates_login_credentials(self):
        # test invalid username and test invalid password cannot login
        invalid_credentials = {'username': 'john_doe',
                               'password': 'nopass'}
        res = self.testHelper.login_user(invalid_credentials)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        self.assertEqual(msg, 'Invalid username or password')


    def test_user_can_logout(self):
        # register user
        self.testHelper.register_user(user_data)
        # login user
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        # logout user
        res = self.testHelper.logout_user(access_token)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        self.assertEqual(msg, "Logged out successfully!")


if __name__ == "__main__":
    unittest.main(module=__name__)
