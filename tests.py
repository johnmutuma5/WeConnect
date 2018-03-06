import unittest
from app.models import Business, User, Review
# from app.exceptions import DuplicationError
import requests, json, re


user_data = {
    "'first_name'": 'John',
    'last_name': 'Doe',
    'gender': 'Male',
    'mobile': '254720000000',
    'email': 'johndoe@gmail.com',
    "username": "john_doe",
    "password": "pass",
}
login_data = {'username': 'john_doe', 'password': 'pass'}
requests = requests.Session() #persist cookies across requests


class TestAPICase (unittest.TestCase):
    def setUp (self):
        self.base_url = 'http://0.0.0.0:8080'
        self.headers = {'content-type': 'application/json'}
        self.register_user (user_data)

    def register_user (self, data):
        url = self.base_url + '/api/v1/auth/register'
        res = requests.post(url, data = json.dumps(user_data), headers = self.headers)
        return res

    def login_user (self, login_data):
        url = self.base_url + '/api/v1/auth/login'
        res = requests.post(url, data = json.dumps(login_data), headers = self.headers)
        return res

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

        match = re.search(pattern, msg)
        logged_user = match.group ('username')
        self.assertEqual (login_data['username'], logged_user)

    def test_user_can_logout (self):
        # login user
        self.login_user (login_data)

        # logout user
        url = self.base_url + '/api/v1/auth/logout'
        res = requests.post(url)
        msg = (res.json())['msg']
        self.assertEqual (msg, "logged out successfully!")

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
