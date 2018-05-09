import unittest, pytest, json, re, time
from app.business.models import Business, Review
from app.user.models import User
from app.exceptions import InvalidUserInputError
from app.tests import BaseAPITestSetUp
from app.tests.dummies import (user_data, user_data2, business_data,
                      invalid_credentials, login_data, login_data2,
                      businesses_data, update_data)


class TestBusinessCase(BaseAPITestSetUp):


    def test_user_can_register_business(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        # register business now
        res = self.testHelper.register_business(business_data, access_token)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        # test actual user from database
        data = business_data['name']
        db_count = self.db_object_count(Business, 'name', data)
        self.assertTrue(db_count == 1)
        # response check
        pattern = r"^SUCCESS[: a-z]+ (?P<business>.+) [a-z!]+$"
        self.assertRegexpMatches(msg, pattern)


    def test_only_logged_in_users_can_register_business(self):
        resp = self.testHelper.register_business(business_data)
        self.assertEqual(resp.status_code, 401)
        resp = self.testHelper.register_business(business_data, 'aninvalid.access.token')
        self.assertEqual(resp.status_code, 401)


    def test_duplicate_businessname_disallowed(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        # register business
        self.testHelper.register_business(business_data, access_token)
        res = self.testHelper.register_business(business_data, access_token)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        self.assertEqual(msg, 'Business name already exists')


    def test_handles_blank_business_name(self):
        self.testHelper.register_user (user_data)
        resp = self.testHelper.login_user (login_data)
        resp_dict = json.loads(resp.data.decode('utf-8'))
        access_token = resp_dict['access_token']
        data_lacking_name = {**business_data, "name": " "}
        res = self.testHelper.register_business (data_lacking_name, access_token)
        resp_dict = json.loads(res.data.decode('utf-8'))
        msg = resp_dict.get("msg")
        self.assertEqual(msg, "Please provide name")


if __name__ == "__main__":
    unittest.main(module=__name__)
