import unittest
from app import Business, User, Review


class TestUserCase (unittest.TestCase):
    def setUp (self):
        self.data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'gender': 'Male',
            'mobile': '254720000000',
            'email': 'johndoe@gmail.com',
            'username': 'john_doe',
            'password': 'a_password',
        }
        self.new_user = User.create_user (self.data)


    def test_create_user (self):
        user = self.new_user
        first_name = self.data['first_name']
        last_name = self.data['last_name']

        data_correct = user.first_name == first_name and user.last_name == last_name
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
