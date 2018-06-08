import unittest
import json
from app.business.models import Business
from app.tests import BaseAPITestSetUp
from app.tests.dummies import(user_data, user_data2, business_data, login_data,
                              login_data2)


class TestBusinessCase(BaseAPITestSetUp):

    def test_only_logged_in_users_can_delete_business(self):
        raw_id = 1000
        resp = self.testHelper.delete_business(raw_id)
        self.assertEqual(resp.status_code, 401)

    def test_handles_deleting_an_unavailble_business(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        resp = self.testHelper.delete_business(10001, access_token)
        res_msg = (json.loads(resp.data.decode("utf-8")))["msg"]
        # test message to match regex
        pattern = r"^UNSUCCESSFUL:.+$"
        self.assertRegexpMatches(res_msg, pattern)

    def test_users_can_delete_business(self):
        self.testHelper.register_user(user_data)
        # login the first user
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.register_business(business_data, access_token)
        # delete business
        resp = self.testHelper.delete_business(1000, access_token)
        # count businesses with id = 1000
        db_count = self.db_object_count(Business, 'id', 1000)
        self.assertTrue(db_count == 0)
        #
        msg = (json.loads(resp.data.decode("utf-8")))["msg"]
        self.assertEqual(msg, "SUCCESS: business deleted")

    def test_users_can_only_delete_their_business(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.register_business(business_data, access_token)
        # logout the current user
        self.testHelper.logout_user(access_token)
        # create a second user`
        self.testHelper.register_user(user_data2)
        res = self.testHelper.login_user(login_data2)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        # try to update and del a business created by the just logged out user
        resp = self.testHelper.delete_business(1000, access_token)
        self.assertEqual(resp.status_code, 403)


if __name__ == "__main__":
    unittest.main(module=__name__)
