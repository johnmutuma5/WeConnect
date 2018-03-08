import unittest
from app.models import Business, User, Review
from app import store
from . import BaseAPITestSetUp
from .dummies import user_data, business_data, invalid_credentials, login_data, businesses_data
import re


class TestAPICase (BaseAPITestSetUp):

    def test_a_user_can_register (self):
        res = self.testHelper.register_user (user_data)
        msg = (res.json())['msg']
        pattern = r"^SUCCESS[: a-z]+ (?P<username>.+) [a-z!]+$"
        self.assertRegexpMatches (msg, pattern)
        # extract username from regular expression
        match = re.search (pattern, msg)
        user_in_response_msg = match.group ('username')
        # assert same as username in data sent
        self.assertEqual (user_in_response_msg, user_data['username'])

    def test_duplicate_username_disallowed (self):
        # register user with similar data as used in setUp
        res = self.testHelper.register_user (user_data)
        msg = (res.json())['msg']
        self.assertEqual (msg, 'Duplicate username not allowed')

    def test_user_can_login (self):
        res = self.testHelper.login_user (login_data)
        msg = (res.json())['msg']

        pattern = r"logged in (?P<username>.+)"
        self.assertRegexpMatches (msg, pattern)
        # extract username from regular expression
        match = re.search(pattern, msg)
        logged_user = match.group ('username')
        self.assertEqual (login_data['username'], logged_user)

    def test_validates_credentials (self):
        res = self.testHelper.login_user (invalid_credentials)
        msg = (res.json())['msg']
        self.assertEqual (msg, 'Invalid username or password')

    def test_user_can_logout (self):
        # login user
        self.testHelper.login_user (login_data)
        # logout user
        res = self.testHelper.logout_user ()
        msg = (res.json())['msg']
        self.assertEqual (msg, "logged out successfully!")

    def test_User_can_register_business (self):
        self.testHelper.login_user (login_data)
        res = self.testHelper.register_business (business_data)
        msg = (res.json())['msg']

        pattern = r"^SUCCESS[: a-z]+ (?P<business>.+) [a-z!]+$"
        self.assertRegexpMatches (msg, pattern)

    def test_duplicate_businessname_disallowed (self):
        res = self.testHelper.register_business (business_data)
        msg = (res.json())['msg']
        self.assertEqual (msg, 'Duplicate business name not allowed')

    def test_users_retrieve_all_businesses (self):
        # register a number of businesses
        for business_data in businesses_data:
            self.testHelper.register_business (business_data)
        # get all businesses info
        res = self.testHelper.get_businesses ()
        res_businesses = (res.json())["businesses"]
        res_business_names = [business_info['name'] for business_info in res_businesses]
        # assert that every piece of information we have sent has been returned
        for data in businesses_data:
            self.assertIn (data['name'], res_business_names)

    def test_users_can_retrieve_one_business (self):
        # we have already stored 3 businesses in a previous test, let's test retrieving one
        raw_id = 5
        res = self.testHelper.get_business (raw_id)
        res_business = (res.json())["business"]
        res_business_id = res_business['id']
        # assert that the response business id equals the url variable
        sent_id = Business.gen_id_string (raw_id)
        self.assertEqual (res_business_id, sent_id)


class TestUserCase (unittest.TestCase):
    def setUp (self):
        self.user_data = user_data
        self.new_user = User.create_user (self.user_data)


    def test_create_user (self):
        user = self.new_user
        first_name = self.user_data['username']
        data_correct = user.username
        self.assertTrue (data_correct)
        #edge case: raises AssertionError for mobile with non int characters
        with self.assertRaises(ValueError):
            self.new_user.mobile = '254725k00000'


class TestBusinessCase (unittest.TestCase):
    def setUp (self):
        self.data = {
            'name': 'Andela',
            'mobile': '254720000000',
            'location': 'TRM',
            'owner': 'John'
        }
        self.new_business = Business.create_business (self.data)


    def test_create_business (self):
        business = self.new_business
        name = self.data['name']
        owner = self.data['owner']
        data_correct = business.name == name and business.owner == owner
        self.assertTrue (data_correct)
        #edge case: raises AssertionError for mobile with non int characters
        with self.assertRaises(ValueError):
            business.mobile = '254725k000000'


class TestReviewCase (unittest.TestCase):
    def setUp (self):
        self.data = {
            'author': 'Alice Doe',
            'business': 'Andela',
            'message': 'They create progressive technology products',
        }
        self.new_review = Review (self.data)

    def test_create_review (self):
        review = self.new_review
        message = self.data['message']
        author = self.data['author']
        data_correct = review.author == author and review.message == message
        self.assertTrue(data_correct)


if __name__ == "__main__":
    unittest.main (module = __name__)
