import unittest
import json
from app.tests import BaseAPITestSetUp
from app.tests.dummies import(user_data, business_data,
                              login_data, businesses_data)


class TestBusinessCase(BaseAPITestSetUp):

    def test_users_retrieve_all_businesses(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        # register a number of businesses(3)
        for business_data in businesses_data:
            self.testHelper.register_business(business_data, access_token)
        # get all businesses info
        res = self.testHelper.get_businesses()
        resp_businesses = (json.loads(res.data.decode("utf-8")))["businesses"]
        # assert that every piece of information we have sent has been returned
        self.assertEqual(len(resp_businesses), len(businesses_data))

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
        resp = self.testHelper.filter_business(filter_dict)
        results = (json.loads(resp.data.decode('utf-8')))['results']
        for result in results:
            search_key = filter_dict['name'].lower()
            business_name = (result['name']).lower()
            self.assertTrue(search_key in business_name)

    def test_filter_applies_pagination(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        for business_data in businesses_data:
            self.testHelper.register_business(business_data, access_token)
        # define a search key
        limit = 2
        filter_dict = {
            "location": "nairobi",
            "limit": limit,
            "page": 1
        }
        resp = self.testHelper.filter_business(filter_dict)
        results = (json.loads(resp.data.decode('utf-8')))['results']
        self.assertTrue(len(results) == limit)

    def test_it_handles_filter_with_invalid_limit_or_page(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        for business_data in businesses_data:
            self.testHelper.register_business(business_data, access_token)
        # define a search key
        filter_dict = {
            "name": "Google",
            "limit": 'ten',
            "page": 1
        }
        resp = self.testHelper.filter_business(filter_dict)
        msg = (json.loads(resp.data.decode('utf-8')))['msg']
        self.assertEqual(msg, 'Invalid pagination limit or page')

    def test_users_can_search_for_business(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        for business_data in businesses_data:
            self.testHelper.register_business(business_data, access_token)
        # define a search key
        search_key = 'lE'
        resp = self.testHelper.search_business(search_key)
        results = (json.loads(resp.data.decode('utf-8')))['results']
        for result in results:
            search_key = search_key.lower()
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
