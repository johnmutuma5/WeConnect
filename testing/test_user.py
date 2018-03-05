import unittest
from app import User

class TestUserCase (unittest.TestCase):
    def setUp (self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'gender': 'Male',
            'mobile': '254720000000',
            'email': 'johndoe@gmail.com',
            'password': 'a_password',
        }
        self.new_user = User.create_user (data)


    def test_create_user (self):
        print ('testing create user')
        user = self.new_user
        data_correct = user.first_name == 'John' and user.last_name == 'Doe'
        self.assertTrue (data_correct)

        #edge case: raises AssertionError for mobile with non int characters
        with self.assertRaises(ValueError):
            self.new_user.mobile = '254725k00000'



def runTestUserCase ():
    # run test cases when imported
    unittest.main (__name__)


if __name__ == "__main__":
    unittest.main ()
