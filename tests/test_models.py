import unittest
from app.v2.models import Business, User, Review
from app.exceptions import InvalidUserInputError

class TestReviewCase (unittest.TestCase):
    def setUp (self):
        self.data = {
            'body': 'They create progressive technology products',
            'heading': 'Wonderful'
        }
        self.test_author_id = 'TST00001'
        self.test_bss_id = 'BUS00001'
        self.new_review = Review.create_review (self.test_bss_id, self.test_author_id, self.data)

    def test_create_review (self):
        review = self.new_review
        heading = self.data['heading']
        data_correct = review.author_id == self.test_author_id and review.heading == heading
        self.assertTrue(data_correct)


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
        supplied_mobile = self.data['mobile']
        data_correct = business.name == name and \
                        business.owner_id == owner_id and \
                        business.mobile == supplied_mobile
        self.assertTrue (data_correct)
        #edge case: raises AssertionError for mobile with non int characters
        with self.assertRaises (InvalidUserInputError):
            business.mobile = '254725k000000'


class TestUserCase (unittest.TestCase):
    def setUp (self):
        self.data = {
            'first_name': 'Lazuli',
            'last_name': 'Murimi',
            'gender': 'Female',
            'email': 'lazuli@gmail.com',
            'mobile': '254728000000',
            'username': 'laz_doe',
            'password': 'pass'
        }
        self.new_user = User.create_user (self.data)

    def test_create_user (self):
        supplied_name = self.data['first_name']
        supplied_username = self.data['username']
        supplied_mobile  = self.data['mobile']
        supplied_email = self.data['email']
        # check data sent in correctly contained
        data_correct = self.new_user.first_name == supplied_name and \
                        self.new_user.username == supplied_username and \
                        self.new_user.mobile == supplied_mobile and \
                        self.new_user.email == supplied_email
        self.assertTrue (data_correct)
        #edge case: raises AssertionError for mobile with non int characters
        with self.assertRaises (InvalidUserInputError):
            self.new_user.mobile = '254725k000000'

    def test_validates_username (self):
        invalid_names = ['000', 'j', '90jdj', 'axc', '    ']
        for name in invalid_names:
            with self.assertRaises (InvalidUserInputError):
                self.new_user.username = name


if __name__ == "__main__":
    unittest.main (module = __name__)
