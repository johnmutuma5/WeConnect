import unittest
import json
import time
from app.tests import BaseAPITestSetUp
from app.tests.dummies import user_data


class TestAPICase (BaseAPITestSetUp):

    def get_password_reset_link(self, username):
        self.testHelper.register_user(user_data)
        reset_data = {"username": username}
        resp = self.testHelper.reset_password(reset_data)
        reset_link = (json.loads(resp.data.decode('utf-8')))['reset_link']
        return reset_link

    def supply_new_password(self, reset_link, reset_data):
        resp = self.testHelper.reset_password_verify(
            reset_link, 'POST', reset_data)
        return resp

    def test_users_can_reset_passwords(self):
        # use username to send password reset request
        username = user_data['username']
        reset_link = self.get_password_reset_link(username)
        # client first clicks link within their email inbox to get update
        # password form
        resp = self.testHelper.reset_password_verify(reset_link)
        msg = (json.loads(resp.data.decode('utf-8')))['msg']
        self.assertEqual(msg, 'Please supply your new password')
        # client fills form a clicks submit to send a post request
        reset_data = {'new_password': "changed"}
        resp = self.supply_new_password(reset_link, reset_data)
        msg = (json.loads(resp.data.decode('utf-8')))['msg']
        self.assertEqual(msg, "Password updated successfully")
        # login with new password
        resp = self.testHelper.login_user({"username": username,
                                           "password": "changed"})
        msg = (json.loads(resp.data.decode('utf-8')))['msg']
        pattern = r"Logged in (?P<username>.+)"
        self.assertRegexpMatches(msg, pattern)

    def test_user_cannot_reset_password_with_expired_token(self):
        username = user_data['username']
        reset_link = self.get_password_reset_link(username)
        # sleep for 1 second; allows development token to expire
        time.sleep(1)
        # client fills form a clicks submit to send a post request
        reset_data = {'new_password': "changed"}
        resp = self.supply_new_password(reset_link, reset_data)
        msg = (json.loads(resp.data.decode('utf-8')))['msg']
        self.assertEqual(msg, "Token expired")

    def test_users_cannot_reset_with_invalid_token(self):
        self.testHelper.register_user(user_data)
        reset_data = {'new_password': "changed"}
        fake_token = "aquitelongstringrepresentingaFAKEtokentoresetpassword"
        fake_link = 'http://127.0.0.1:8080/api/v2/auth/reset-password/verify?t='\
            + fake_token
        resp = self.testHelper.reset_password_verify(
            fake_link, 'POST', reset_data)
        msg = (json.loads(resp.data.decode('utf-8')))['msg']
        self.assertEqual(msg, "Invalid token")
        # test users can

    def test_users_cannot_reset_password_with_unknown_or_no_username(self):
        invalid_usernames = ['unknown_doe', None]
        for username in invalid_usernames:
            reset_data = {"username": username}
            resp = self.testHelper.reset_password(reset_data)
            msg = (json.loads(resp.data.decode('utf-8')))['msg']
            if username:
                self.assertEqual(msg, 'Invalid Username')
            else:
                self.assertEqual(msg, 'Please supply your username')


if __name__ == "__main__":
    unittest.main(module=__name__)
