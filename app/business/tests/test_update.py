import unittest
import json
from app.tests import BaseAPITestSetUp
from app.tests.dummies import(user_data, user_data2, business_data, login_data,
                              login_data2, businesses_data, update_data)


class TestBusinessCase(BaseAPITestSetUp):

    def test_users_can_update_business_info(self):
        raw_id = 1000
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.register_business(business_data, access_token)
        # update business
        self.testHelper.update_business(raw_id, update_data, access_token)
        # get the business's info in it's new state
        res = self.testHelper.get_business(raw_id)
        res_business_info = (json.loads(res.data.decode("utf-8")))["info"]
        self.assertEqual(update_data['location'], res_business_info['location'])

    def test_only_logged_in_users_can_update_business(self):
        raw_id = 1000
        # try update without an access token
        resp = self.testHelper.update_business(raw_id, update_data)
        self.assertEqual(resp.status_code, 401)

    def test_users_cannot_update_with_existing_business_names(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.register_business(business_data, access_token)
        # register another businesses: business_data[1] has name Google
        self.testHelper.register_business(businesses_data[1], access_token)
        # try to update first business with name Google
        name_update_data = {"name": "Google"}
        resp = self.testHelper.update_business(
            1000, name_update_data, access_token)
        msg = (json.loads(resp.data.decode('utf-8')))['msg']
        self.assertEqual(msg, "Duplicate business name not allowed")

    def test_users_cannot_update_with_blank_names(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.register_business(business_data, access_token)
        # register another businesses: business_data[1] has name Google
        self.testHelper.register_business(businesses_data[1], access_token)
        # try to update first business with name Google
        name_update_data = {"name": "  "}
        resp = self.testHelper.update_business(
            1000, name_update_data, access_token)
        msg = (json.loads(resp.data.decode('utf-8')))['msg']
        self.assertEqual(msg, "Please provide name")


    def test_users_cannot_update_with_unknown_properties(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.register_business(business_data, access_token)
        # register another businesses: business_data[1] has name Google
        self.testHelper.register_business(businesses_data[1], access_token)
        # try to update first business with name Google
        unknown_prop = 'namse'
        unknown_data = {unknown_prop: "set this"}
        resp = self.testHelper.update_business(
            1000, unknown_data, access_token)
        msg = (json.loads(resp.data.decode('utf-8')))['msg']
        self.assertEqual(msg, "Unknown property %s"%unknown_prop)


    def test_handles_updating_an_unavailble_business(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        # update with an unavailable id
        name_update_data = {"name": "Google"}
        resp = self.testHelper.update_business(
            10001, name_update_data, access_token)
        res_msg = (json.loads(resp.data.decode("utf-8")))["msg"]
        # test message to match regex
        pattern = r"^UNSUCCESSFUL:.+$"
        self.assertRegexpMatches(res_msg, pattern)

    def test_users_can_only_update_their_business(self):
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
        resp = self.testHelper.update_business(1000, update_data, access_token)
        self.assertEqual(resp.status_code, 403)


if __name__ == "__main__":
    unittest.main(module=__name__)
