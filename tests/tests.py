import unittest
from app.models import Business, User, Review
from . import BaseAPITestSetUp, TestHelpers
from .dummies import user_data, business_data, invalid_credentials, login_data
import re


class TestAPICase (BaseAPITestSetUp, TestHelpers):
    def test_duplicate_username_disallowed (self):
        # register user with similar data as used in setUp
        res = self.register_user (user_data)
        msg = (res.json())['msg']
        self.assertEqual (msg, 'Duplicate username not allowed')

    def test_user_can_login (self):
        res = self.login_user (login_data)
        msg = (res.json())['msg']

        pattern = r"logged in (?P<username>.+)"
        self.assertRegexpMatches (msg, pattern)
        # extract username from regular expression
        match = re.search(pattern, msg)
        logged_user = match.group ('username')
        self.assertEqual (login_data['username'], logged_user)

    def test_validates_credentials (self):
        res = self.login_user (invalid_credentials)
        msg = (res.json())['msg']
        self.assertEqual (msg, 'Invalid username or password')

    def test_user_can_logout (self):
        # login user
        self.login_user (login_data)
        # logout user
        res = self.logout_user ()
        msg = (res.json())['msg']
        self.assertEqual (msg, "logged out successfully!")

    def test_User_can_register_business (self):
        self.login_user (login_data)
        res = self.register_business (business_data)
        msg = (res.json())['msg']

        pattern = r"^SUCCESS: (?P<business>.+) \w+!$"
        self.assertRegexpMatches (msg, pattern)

    def test_duplicate_businessname_disallowed (self):
        res = self.register_business (business_data)
        msg = (res.json())['msg']
        self.assertEqual (msg, 'Duplicate business name not allowed')


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
