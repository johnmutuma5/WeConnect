import unittest
from app import User

class TestUserCase (unittest.TestCase):

    def test_create_user (self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'gender': 'Male',
            'mobile': '0720000000',
            'email': 'johndoe@gmail.com',
            'password': 'a_password',
        }
        new_user = User.create_user (data)
        data_correct = new_user.first_name == 'John' and new_user.last_name == 'Doe'
        self.assertTrue (data_correct)





def runTestUserCase ():
    unittest.main ()
