import unittest, pytest, json
from app.models import Business, User, Review
from app.exceptions import InvalidUserInputError
from app import store
from . import BaseAPITestSetUp
from .dummies import (user_data, user_data2, business_data,
                        invalid_credentials, login_data, login_data2,
                        businesses_data, update_data, review_data)
import re


class TestAPICase (BaseAPITestSetUp):
    # @pytest.mark.run(order = 1)
    def test_a_user_can_register (self):
        res = self.testHelper.register_user (user_data)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        pattern = r"^SUCCESS[: a-z]+ (?P<username>.+) [a-z!]+$"
        self.assertRegexpMatches (msg, pattern)
        # extract username from regular expression
        match = re.search (pattern, msg)
        user_in_response_msg = match.group ('username')
        # assert same as username in data sent
        self.assertEqual (user_in_response_msg, user_data['username'])

    # @pytest.mark.run(order = 2)
    def test_duplicate_username_disallowed (self):
        res = self.testHelper.register_user (user_data)
        # register user with similar data as used in setUp
        res = self.testHelper.register_user (user_data)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        self.assertEqual (msg, 'Username already exists')
    #
    # @pytest.mark.run(order = 3)
    def test_user_can_login (self):
        res = self.testHelper.register_user (user_data)
        res = self.testHelper.login_user (login_data)
        msg = (json.loads(res.data.decode("utf-8")))['msg']

        pattern = r"Logged in (?P<username>.+)"
        self.assertRegexpMatches (msg, pattern)
        # extract username from regular expression
        match = re.search(pattern, msg)
        logged_user = match.group ('username')
        self.assertEqual (login_data['username'], logged_user)
    #
    # @pytest.mark.run(order = 4)
    def test_validates_credentials (self):
        res = self.testHelper.login_user (invalid_credentials)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        self.assertEqual (msg, 'Invalid username or password')
    #
    # @pytest.mark.run(order = 5)
    def test_user_can_logout (self):
        # register user
        self.testHelper.register_user (user_data)
        # login user
        self.testHelper.login_user (login_data)
        # logout user
        res = self.testHelper.logout_user ()
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        self.assertEqual (msg, "Logged out successfully!")
    # #
    # @pytest.mark.run(order = 6)
    def test_user_can_register_business (self):
        self.testHelper.register_user (user_data)
        self.testHelper.login_user (login_data)
        res = self.testHelper.register_business (business_data)
        msg = (json.loads(res.data.decode("utf-8")))['msg']

        pattern = r"^SUCCESS[: a-z]+ (?P<business>.+) [a-z!]+$"
        self.assertRegexpMatches (msg, pattern)
    # #
    # @pytest.mark.run(order = 7)
    def test_duplicate_businessname_disallowed (self):
        self.testHelper.register_user (user_data)
        self.testHelper.login_user (login_data)
        self.testHelper.register_business (business_data)
        res = self.testHelper.register_business (business_data)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        self.assertEqual (msg, 'Duplicate business name not allowed')
    # #
    # @pytest.mark.run(order = 8)
    def test_users_retrieve_all_businesses (self):
        self.testHelper.register_user (user_data)
        self.testHelper.login_user (login_data)
        # register a number of businesses
        for business_data in businesses_data:
            self.testHelper.register_business (business_data)
        # get all businesses info
        res = self.testHelper.get_businesses ()
        res_businesses = (json.loads(res.data.decode("utf-8")))["businesses"]
        res_business_names = [business_info['name'] for business_info in res_businesses]
        # assert that every piece of information we have sent has been returned
        for data in businesses_data:
            self.assertIn (data['name'], res_business_names)
    #
    # @pytest.mark.run(order = 9)
    def test_users_retrieve_one_business (self):
        self.testHelper.register_user (user_data)
        self.testHelper.login_user (login_data)
        # register a number of businesses
        self.testHelper.register_business (business_data)
        raw_id = 1
        res = self.testHelper.get_business (raw_id)
        res_business_info = (json.loads(res.data.decode("utf-8")))["info"]
        print(res_business_info)
        res_business_id = res_business_info['id']
        # assert that the response business id equals the url variable
        sent_id = Business.gen_id_string (raw_id)
        self.assertEqual (res_business_id, sent_id)
    #
    # @pytest.mark.run(order = 10)
    def test_users_retrieve_only_avail_business (self):
        raw_id = 1000000
        res = self.testHelper.get_business (raw_id)
        res_msg= (json.loads(res.data.decode("utf-8")))["msg"]
        # test message to match regex
        pattern = r"^UNSUCCESSFUL:.+$"
        self.assertRegexpMatches (res_msg, pattern)
    #
    # @pytest.mark.run(order = 11)
    def test_users_update_a_business (self):
        raw_id = 1
        self.testHelper.register_user (user_data)
        self.testHelper.login_user (login_data)
        self.testHelper.register_business (business_data)
        self.testHelper.update_business (raw_id, update_data)
        # get the business's info in it's new state
        res = self.testHelper.get_business (raw_id)
        res_business_info = (json.loads(res.data.decode("utf-8")))["info"]

        for key, value in update_data.items():
            self.assertEqual (update_data[key], res_business_info[key])
    #
    # @pytest.mark.run(order = 12)
    def test_users_can_only_update_their_business (self):
        self.testHelper.register_user (user_data)
        self.testHelper.login_user (login_data)
        self.testHelper.register_business (business_data)
        # logout the current user
        self.testHelper.logout_user ()
        # create a second user`
        self.testHelper.register_user (user_data2)
        self.testHelper.login_user (login_data2)
        # try to update one of the three businesses created by the just logged out user
        resp = self.testHelper.update_business (1, update_data)
        self.assertEqual (resp.status_code, 401)
    #
    # @pytest.mark.run(order = 13)
    def test_users_can_delete_business (self):
        self.testHelper.register_user (user_data)
        # login the first user
        self.testHelper.login_user (login_data)
        self.testHelper.register_business (business_data)
        # delete business
        resp = self.testHelper.delete_business (1)
        msg = (json.loads(resp.data.decode("utf-8")))["msg"]
        self.assertEqual (msg, "SUCCESS: business deleted")
    #
    # @pytest.mark.run(order = 14)
    def test_users_can_make_a_review (self):
        self.testHelper.register_user (user_data)
        self.testHelper.register_user (user_data2)
        # login the first user
        self.testHelper.login_user (login_data)
        self.testHelper.register_business (business_data)
        self.testHelper.logout_user ()
        # login second user
        self.testHelper.login_user (login_data2)
        # second user make a review
        resp = self.testHelper.make_review (1, review_data[0])
        msg = (json.loads(resp.data.decode("utf-8")))["msg"]
        #extract posted review heading from message
        pattern = r"\w+:\[(?P<heading>.+)\] "
        match = re.search (pattern, msg)
        posted_review_heading = match.group ("heading")
        self.assertEqual (posted_review_heading, review_data[0]['heading'])
        self.testHelper.logout_user ()
    #
    # @pytest.mark.run(order = 15)
    def test_user_can_get_reviews (self):
        self.testHelper.register_user (user_data)
        self.testHelper.register_user (user_data2)
        self.testHelper.login_user (login_data)
        self.testHelper.register_business (business_data)
        self.testHelper.make_review (1, review_data[0])
        self.testHelper.logout_user ()
        #login another user
        self.testHelper.login_user (login_data2)
        self.testHelper.make_review (1, review_data[1])
        resp = self.testHelper.get_all_reviews (1)
        reviews_info = (json.loads(resp.data.decode("utf-8")))['info']
        resp_review_headings = [review_info['heading'] for review_info in reviews_info]
        # check that all review heading have been returned
        for data in review_data:
            self.assertIn (data['heading'], resp_review_headings)




#
class TestBusinessCase (unittest.TestCase):
    def setUp (self):
        self.data = {
            'name': 'Andela',
            'mobile': '254720000000',
            'location': 'TRM',
            'owner': 'John',
        }
        self.test_id = 'TST00001'
        self.new_business = Business.create_business (self.data, self.test_id)


    def test_create_business (self):
        business = self.new_business
        name = self.data['name']
        owner_id = self.test_id
        data_correct = business.name == name and business.owner_id == owner_id
        self.assertTrue (data_correct)
        #edge case: raises AssertionError for mobile with non int characters
        with self.assertRaises (InvalidUserInputError):
            business.mobile = '254725k000000'


class TestReviewCase (unittest.TestCase):
    def setUp (self):
        self.data = {
            'body': 'They create progressive technology products',
            'heading': 'Wonderful'
        }
        self.test_author_id = 'TST00001'
        self.test_bss_id = 'BUS00001'
        self.new_review = Review (self.test_bss_id, self.test_author_id, self.data)

    def test_create_review (self):
        review = self.new_review
        heading = self.data['heading']
        data_correct = review.author_id == self.test_author_id and review.heading == heading
        self.assertTrue(data_correct)


if __name__ == "__main__":
    unittest.main (module = __name__)