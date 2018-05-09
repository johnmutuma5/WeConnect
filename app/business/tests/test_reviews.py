import unittest, pytest, json, re, time
from app.business.models import Business, Review
from app.user.models import User
from app.exceptions import InvalidUserInputError
from app.tests import BaseAPITestSetUp
from app.tests.dummies import (user_data, user_data2, business_data,
                      invalid_credentials, login_data, login_data2,
                      businesses_data, update_data, review_data)


class TestBusinessCase(BaseAPITestSetUp):

    def test_users_retrieve_only_avail_business_reviews(self):
        raw_id = 1000000
        resp = self.testHelper.get_all_reviews(raw_id)
        res_msg = (json.loads(resp.data.decode("utf-8")))["msg"]
        # test message to match regex
        pattern = r"^UNSUCCESSFUL:.+$"
        self.assertRegexpMatches(res_msg, pattern)


    def test_users_can_make_a_review(self):
        self.testHelper.register_user(user_data)
        self.testHelper.register_user(user_data2)
        # login the first user
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.register_business(business_data, access_token)
        self.testHelper.logout_user(access_token)
        # login second user
        res = self.testHelper.login_user(login_data2)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        # second user make a review
        resp = self.testHelper.make_review(1000, review_data[0], access_token)
        # check count of review with sent heading in db
        posted_heading = review_data[0]['heading']
        db_count = self.db_object_count(Review, 'heading', posted_heading)
        self.assertEqual(db_count, 1)
        # test response message
        msg = (json.loads(resp.data.decode("utf-8")))["msg"]
        pattern = r"^SUCCESS:.+$"
        self.assertRegexpMatches(msg, pattern)
        self.testHelper.logout_user(access_token)


    def test_user_can_get_reviews(self):
        self.testHelper.register_user(user_data)
        self.testHelper.register_user(user_data2)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.register_business(business_data, access_token)
        self.testHelper.make_review(1000, review_data[0], access_token)
        self.testHelper.logout_user(access_token)
        # login another user
        res = self.testHelper.login_user(login_data2)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.make_review(1000, review_data[1], access_token)
        resp = self.testHelper.get_all_reviews(1000)
        reviews_info = (json.loads(resp.data.decode("utf-8")))['info']
        resp_review_headings = [review_info['heading']
                                for review_info in reviews_info]
        # check that all review heading have been returned
        for data in review_data:
            self.assertIn(data['heading'], resp_review_headings)


if __name__ == "__main__":
    unittest.main(module=__name__)
