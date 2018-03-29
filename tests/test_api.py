import unittest, pytest, json
from app.v2.models import Business, User, Review
from app.exceptions import InvalidUserInputError
from app.v2 import store
from . import BaseAPITestSetUp
from .dummies import (user_data, user_data2, business_data,
                        invalid_credentials, login_data, login_data2,
                        businesses_data, update_data, review_data)
import re


class TestAPICase (BaseAPITestSetUp):

    def confirm_object_persisted (self, Obj_model, col_name, value):
        session = store.Session ()
        stored_obj = session.query(getattr(Obj_model, col_name))\
                            .filter(getattr(Obj_model, col_name) == value)\
                            .all()
        self.assertEqual (len(stored_obj), 1)
        session.close ()

    def test_a_user_can_register (self):
        res = self.testHelper.register_user (user_data)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        # test actual user from database
        data = user_data['username']
        self.confirm_object_persisted(User, 'username', data)
        # response check
        pattern = r"^SUCCESS[: a-z]+ (?P<username>.+) [a-z!]+$"
        self.assertRegexpMatches (msg, pattern)
        # response check: confirm correct username
        match = re.search (pattern, msg)
        user_in_response_msg = match.group ('username')
        self.assertEqual (user_in_response_msg, user_data['username'])

    # @pytest.mark.run(order = 2)
    def test_duplicate_username_disallowed (self):
        res = self.testHelper.register_user (user_data)
        # register user with similar data as used above
        res = self.testHelper.register_user (user_data)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        self.assertEqual (msg, 'Username already exists')

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

    # @pytest.mark.run(order = 4)
    def test_validates_credentials (self):
        # test invalid username and test invalid password
        invalid_logins = [
                            invalid_credentials,
                            {'username': 'john_doe', 'password': 'nopass'}]
        for invalid_login in invalid_logins:
            res = self.testHelper.login_user (invalid_login)
            msg = (json.loads(res.data.decode("utf-8")))['msg']
            self.assertEqual (msg, 'Invalid username or password')

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

    # @pytest.mark.run(order = 6)
    def test_user_can_register_business (self):
        self.testHelper.register_user (user_data)
        self.testHelper.login_user (login_data)
        res = self.testHelper.register_business (business_data)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        # test actual user from database
        data = business_data['name']
        self.confirm_object_persisted(Business, 'name', data)
        # response check
        pattern = r"^SUCCESS[: a-z]+ (?P<business>.+) [a-z!]+$"
        self.assertRegexpMatches (msg, pattern)

    # @pytest.mark.run(order = 7)
    def test_duplicate_businessname_disallowed (self):
        self.testHelper.register_user (user_data)
        self.testHelper.login_user (login_data)
        self.testHelper.register_business (business_data)
        res = self.testHelper.register_business (business_data)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        self.assertEqual (msg, 'Business name already exists')

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

    @pytest.mark.run(order = 9)
    def test_users_retrieve_one_business (self):
        self.testHelper.register_user (user_data)
        self.testHelper.login_user (login_data)
        # register a number of businesses
        self.testHelper.register_business (business_data)
        raw_id = 1000
        res = self.testHelper.get_business (raw_id)
        res_business_info = (json.loads(res.data.decode("utf-8")))["info"]
        print(res_business_info)
        res_business_id = res_business_info['id']
        # assert that the response business id equals the url variable
        self.assertEqual (res_business_id, 1000)

    # @pytest.mark.run(order = 10)
    def test_users_retrieve_only_avail_business (self):
        raw_id = 1000000
        res = self.testHelper.get_business (raw_id)
        res_msg= (json.loads(res.data.decode("utf-8")))["msg"]
        # test message to match regex
        pattern = r"^UNSUCCESSFUL:.+$"
        self.assertRegexpMatches (res_msg, pattern)

    # @pytest.mark.run(order = 11)
    def test_users_can_update_business_info (self):
        raw_id = 1000
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
#     def test_users_cannot_update_with_existing_business_names (self):
#         self.testHelper.register_user (user_data)
#         self.testHelper.login_user (login_data)
#         self.testHelper.register_business (business_data)
#         # register another businesses
#         self.testHelper.register_business (businesses_data[1])
#         name_update_data = {"name": "Google"}
#         resp = self.testHelper.update_business(1, name_update_data)
#         msg = (json.loads(resp.data.decode('utf-8')))['msg']
#         self.assertEqual (msg, "Duplicate business name not allowed")
#     #
#     # @pytest.mark.run(order = 12)
#     def test_users_can_only_update_their_business (self):
#         self.testHelper.register_user (user_data)
#         self.testHelper.login_user (login_data)
#         self.testHelper.register_business (business_data)
#         # logout the current user
#         self.testHelper.logout_user ()
#         # create a second user`
#         self.testHelper.register_user (user_data2)
#         self.testHelper.login_user (login_data2)
#         # try to update one of the three businesses created by the just logged out user
#         resp = self.testHelper.update_business (1, update_data)
#         self.assertEqual (resp.status_code, 401)
#     #
#     # @pytest.mark.run(order = 13)
#     def test_users_can_delete_business (self):
#         self.testHelper.register_user (user_data)
#         # login the first user
#         self.testHelper.login_user (login_data)
#         self.testHelper.register_business (business_data)
#         # delete business
#         resp = self.testHelper.delete_business (1)
#         msg = (json.loads(resp.data.decode("utf-8")))["msg"]
#         self.assertEqual (msg, "SUCCESS: business deleted")
#     #
#     # @pytest.mark.run(order = 14)
#     def test_users_can_make_a_review (self):
#         self.testHelper.register_user (user_data)
#         self.testHelper.register_user (user_data2)
#         # login the first user
#         self.testHelper.login_user (login_data)
#         self.testHelper.register_business (business_data)
#         self.testHelper.logout_user ()
#         # login second user
#         self.testHelper.login_user (login_data2)
#         # second user make a review
#         resp = self.testHelper.make_review (1, review_data[0])
#         msg = (json.loads(resp.data.decode("utf-8")))["msg"]
#         #extract posted review heading from message
#         pattern = r"\w+:\[(?P<heading>.+)\] "
#         match = re.search (pattern, msg)
#         posted_review_heading = match.group ("heading")
#         self.assertEqual (posted_review_heading, review_data[0]['heading'])
#         self.testHelper.logout_user ()
#     #
#     # @pytest.mark.run(order = 15)
#     def test_user_can_get_reviews (self):
#         self.testHelper.register_user (user_data)
#         self.testHelper.register_user (user_data2)
#         self.testHelper.login_user (login_data)
#         self.testHelper.register_business (business_data)
#         self.testHelper.make_review (1, review_data[0])
#         self.testHelper.logout_user ()
#         #login another user
#         self.testHelper.login_user (login_data2)
#         self.testHelper.make_review (1, review_data[1])
#         resp = self.testHelper.get_all_reviews (1)
#         reviews_info = (json.loads(resp.data.decode("utf-8")))['info']
#         resp_review_headings = [review_info['heading'] for review_info in reviews_info]
#         # check that all review heading have been returned
#         for data in review_data:
#             self.assertIn (data['heading'], resp_review_headings)
#
#     def test_users_can_reset_password (self):
#         self.testHelper.register_user (user_data)
#         # use username to send password reset request
#         username = user_data['username']
#         reset_data = {"username": username}
#         resp = self.testHelper.reset_password (reset_data)
#         token = (json.loads(resp.data.decode ('utf-8')))['t']
#         # supply a new password
#         reset_data = {'new_password': "changed"}
#         resp = self.testHelper.reset_password (reset_data, token)
#         msg = (json.loads (resp.data.decode ('utf-8')))['msg']
#         self.assertEqual (msg, "Password updated successfully")
#         # login with new password
#         resp = self.testHelper.login_user ({"username": username,
#                                         "password": "changed"})
#         msg = (json.loads (resp.data.decode('utf-8')))['msg']
#         pattern = r"Logged in (?P<username>.+)"
#         self.assertRegexpMatches (msg, pattern)
#         # test users cannot use an invalid token
#         token = r"aquitelongstringrepresentingatokentoresetpassword"
#         resp = self.testHelper.reset_password (reset_data, token)
#         msg = (json.loads (resp.data.decode ('utf-8')))['msg']
#         self.assertEqual (msg, "Invalid token")
#
#

#

if __name__ == "__main__":
    unittest.main (module = __name__)
