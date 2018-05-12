import unittest
import json
import re
from app.user.models import User
from app.tests import BaseAPITestSetUp
from app.tests.dummies import user_data, user_data2


class TestAPICase (BaseAPITestSetUp):

    def test_a_user_can_register(self):
        url = self.base_url + '/api/v2/auth/register'
        res = self.app.post(url, data=json.dumps(
            user_data), headers=self.headers)

        msg = (json.loads(res.data.decode("utf-8")))['msg']
        # test actual user from database
        data = user_data['username']
        db_count = self.db_object_count(User, 'username', data)
        self.assertTrue(db_count == 1)
        # response check
        pattern = r"^SUCCESS[: a-z]+ (?P<username>.+) [a-z!]+$"
        self.assertRegexpMatches(msg, pattern)
        # response check: confirm correct username
        match = re.search(pattern, msg)
        user_in_response_msg = match.group('username')
        self.assertEqual(user_in_response_msg, user_data['username'])

    def test_user_cannot_register_with_invalid_username(self):
        invalid_names = ['000', '90jdj', 'axc']
        for invalid_name in invalid_names:
            # make a copy of valid user_data by unpacking and replace username
            # with invalid_name
            invalid_user_data = {**user_data, "username": invalid_name}
            # send request with invalid_user_data
            res = self.testHelper.register_user(invalid_user_data)
            msg = (json.loads(res.data.decode("utf-8")))['msg']
            self.assertEqual(msg, 'Invalid username!')

    def test_user_cannot_register_with_invalid_email(self):
        invalid_email_data = {**user_data, 'email': 'john.doe@'}
        resp = self.testHelper.register_user(invalid_email_data)
        resp_dict = json.loads(resp.data.decode('utf-8'))
        msg = resp_dict['msg']
        self.assertEqual(msg, 'Invalid email')

    # @pytest.mark.run(order = 2)
    def test_duplicate_username_disallowed(self):
        res = self.testHelper.register_user(user_data)
        # register user with similar data as used above but different email
        identical_email = {**user_data, "email": 'another@gmail.com'}
        res = self.testHelper.register_user(identical_email)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        self.assertEqual(msg, 'Username already exists')

    def test_checks_cases_to_determine_duplication(self):
        res = self.testHelper.register_user(user_data)
        test_data_caps = {
            **user_data,
            "email": "another@gmail.com",
            "username": 'JOHN_DOE'}
        res = self.testHelper.register_user(test_data_caps)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        self.assertEqual(msg, 'Username already exists')

    def test_duplicate_emails_disallowed(self):
        res = self.testHelper.register_user(user_data)
        # make a copy of user data and change the username, leave email as is
        changed_username = {**user_data2, "email": "Johndoe@gmail.com"}
        res = self.testHelper.register_user(changed_username)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        self.assertEqual(msg, 'Email already exists')


if __name__ == "__main__":
    unittest.main(module=__name__)
