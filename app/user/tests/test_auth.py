import unittest, pytest, json, re, time
from app.business.models import Business, Review
from app.user.models import User
from app.exceptions import InvalidUserInputError
from app.tests import BaseAPITestSetUp
from app.tests.dummies import (user_data, user_data2, business_data,
                      invalid_credentials, login_data, login_data2,
                      businesses_data, update_data, review_data)


class TestAPICase (BaseAPITestSetUp):

    def test_user_can_login(self):
        res = self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        msg = (json.loads(res.data.decode("utf-8")))['msg']

        pattern = r"Logged in (?P<username>.+)"
        self.assertRegexpMatches(msg, pattern)
        # extract username from regular expression
        match = re.search(pattern, msg)
        logged_user = match.group('username')
        self.assertEqual(login_data['username'], logged_user)

    # @pytest.mark.run(order = 4)
    def test_validates_credentials(self):
        # test invalid username and test invalid password
        invalid_logins = [
            invalid_credentials,
            {'username': 'john_doe', 'password': 'nopass'}]
        for invalid_login in invalid_logins:
            res = self.testHelper.login_user(invalid_login)
            msg = (json.loads(res.data.decode("utf-8")))['msg']
            self.assertEqual(msg, 'Invalid username or password')

    # @pytest.mark.run(order = 5)
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
