import unittest, json
from app.tests import BaseAPITestSetUp
from app.tests.dummies import (user_data, business_data,
                      login_data,
                      businesses_data, update_data)


class TestBusinessCase(BaseAPITestSetUp):

    def test_users_retrieve_all_businesses(self):
        self.testHelper.register_user(user_data)
        res=self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        # register a number of businesses
        for business_data in businesses_data:
            self.testHelper.register_business(business_data, access_token)
        # get all businesses info
        res = self.testHelper.get_businesses()
        res_businesses = (json.loads(res.data.decode("utf-8")))["businesses"]
        res_business_names = [business_info['name']
                              for business_info in res_businesses]
        # assert that every piece of information we have sent has been returned
        for data in businesses_data:
            self.assertIn(data['name'], res_business_names)


    def test_users_retrieve_one_business(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        # register a number of businesses
        self.testHelper.register_business(business_data, access_token)
        raw_id = 1000
        res = self.testHelper.get_business(raw_id)
        res_business_info = (json.loads(res.data.decode("utf-8")))["info"]
        res_business_id = res_business_info['id']
        # assert that the response business id equals the url variable
        self.assertEqual(res_business_id, 1000)


    def test_users_can_filter_businesses(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        for business_data in businesses_data:
            self.testHelper.register_business(business_data, access_token)
        # define a search key
        filter_dict = {
            "name": "Google",
            "location": "Nairobi",
            "category": "Technology"
        }
        resp = self.testHelper.search_business(filter_dict)
        results = (json.loads(resp.data.decode('utf-8')))['results']
        for result in results:
            search_key = filter_dict['name'].lower()
            business_name = (result['name']).lower()
            self.assertTrue(search_key in business_name)


    def test_users_retrieve_only_avail_business_info(self):
        raw_id = 1000000
        resp = self.testHelper.get_business(raw_id)
        res_msg = (json.loads(resp.data.decode("utf-8")))["msg"]
        # test message to match regex
        pattern = r"^UNSUCCESSFUL:.+$"
        self.assertRegexpMatches(res_msg, pattern)


if __name__ == "__main__":
    unittest.main(module=__name__)
