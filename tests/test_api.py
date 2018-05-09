import unittest, pytest, json, re, time
from sqlalchemy import func
from app.business.models import Business, Review
from app.user.models import User
from app.exceptions import InvalidUserInputError
from . import BaseAPITestSetUp
from .dummies import (user_data, user_data2, business_data,
                      invalid_credentials, login_data, login_data2,
                      businesses_data, update_data, review_data)


class TestAPICase (BaseAPITestSetUp):
    @staticmethod
    def db_object_count(Obj_model, col_name, value):
        session = store.Session()
        count = session.query(func.COUNT(getattr(Obj_model, col_name)))\
            .filter(getattr(Obj_model, col_name) == value)\
            .scalar()
        session.close()
        return count

    def test_a_user_can_register(self):
        res = self.testHelper.register_user(user_data)
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
            # make a copy of valid user_data by unpacking and replace username with invalid_name
            invalid_user_data = {**user_data, "username": invalid_name}
            # send request with invalid_user_data
            res = self.testHelper.register_user(invalid_user_data)
            msg = (json.loads(res.data.decode("utf-8")))['msg']
            self.assertEqual(msg, 'Invalid username!')


    def test_user_cannot_register_with_invalid_email(self):
        invalid_email_data = {**user_data, 'email':'john.doe@'}
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
        test_data_caps = {**user_data, "email":"another@gmail.com", "username": 'JOHN_DOE'}
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


    # @pytest.mark.run(order = 3)
    def test_user_can_login(self):
        res = self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        msg = (json.loads(res.data.decode("utf-8")))['msg']

        pattern = r"Logged in (?P<username>.+)"
        self.assertRegexpMatches(msg, pattern)
        # extract username from regular expression
        match = re.search(pattern, msg)
        logged_user = match.group('username')
        self.assertEqual(login_data['username'], logged_user)

    # @pytest.mark.run(order = 4)
    def test_validates_credentials(self):
        # test invalid username and test invalid password
        invalid_logins = [
            invalid_credentials,
            {'username': 'john_doe', 'password': 'nopass'}]
        for invalid_login in invalid_logins:
            res = self.testHelper.login_user(invalid_login)
            msg = (json.loads(res.data.decode("utf-8")))['msg']
            self.assertEqual(msg, 'Invalid username or password')

    # @pytest.mark.run(order = 5)
    def test_user_can_logout(self):
        # register user
        self.testHelper.register_user(user_data)
        # login user
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        # logout user
        res = self.testHelper.logout_user(access_token)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        self.assertEqual(msg, "Logged out successfully!")

    # @pytest.mark.run(order = 6)
    def test_user_can_register_business(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        # register business now
        res = self.testHelper.register_business(business_data, access_token)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        # test actual user from database
        data = business_data['name']
        db_count = self.db_object_count(Business, 'name', data)
        self.assertTrue(db_count == 1)
        # response check
        pattern = r"^SUCCESS[: a-z]+ (?P<business>.+) [a-z!]+$"
        self.assertRegexpMatches(msg, pattern)


    def test_only_logged_in_users_can_register_business(self):
        resp = self.testHelper.register_business(business_data)
        self.assertEqual(resp.status_code, 401)
        resp = self.testHelper.register_business(business_data, 'aninvalid.access.token')
        self.assertEqual(resp.status_code, 401)


    # @pytest.mark.run(order = 7)
    def test_duplicate_businessname_disallowed(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        # register business
        self.testHelper.register_business(business_data, access_token)
        res = self.testHelper.register_business(business_data, access_token)
        msg = (json.loads(res.data.decode("utf-8")))['msg']
        self.assertEqual(msg, 'Business name already exists')


    def test_handles_blank_business_name(self):
        self.testHelper.register_user (user_data)
        resp = self.testHelper.login_user (login_data)
        resp_dict = json.loads(resp.data.decode('utf-8'))
        access_token = resp_dict['access_token']
        data_lacking_name = {**business_data, "name": " "}
        res = self.testHelper.register_business (data_lacking_name, access_token)
        resp_dict = json.loads(res.data.decode('utf-8'))
        msg = resp_dict.get("msg")
        self.assertEqual(msg, "Please provide name")


    # @pytest.mark.run(order = 8)
    def test_users_retrieve_all_businesses(self):
        self.testHelper.register_user(user_data)
        res=self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        # register a number of businesses
        for business_data in businesses_data:
            self.testHelper.register_business(business_data, access_token)
        # get all businesses info
        res = self.testHelper.get_businesses()
        res_businesses = (json.loads(res.data.decode("utf-8")))["businesses"]
        res_business_names = [business_info['name']
                              for business_info in res_businesses]
        # assert that every piece of information we have sent has been returned
        for data in businesses_data:
            self.assertIn(data['name'], res_business_names)

    # @pytest.mark.run(order=9)
    def test_users_retrieve_one_business(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        # register a number of businesses
        self.testHelper.register_business(business_data, access_token)
        raw_id = 1000
        res = self.testHelper.get_business(raw_id)
        res_business_info = (json.loads(res.data.decode("utf-8")))["info"]
        res_business_id = res_business_info['id']
        # assert that the response business id equals the url variable
        self.assertEqual(res_business_id, 1000)

    def test_users_can_search_for_business(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        for business_data in businesses_data:
            self.testHelper.register_business(business_data, access_token)
        # define a search key
        search_key = 'lE'
        resp = self.testHelper.search_business(search_key)
        results = (json.loads(resp.data.decode('utf-8')))['results']
        for result in results:
            search_key = search_key.lower()
            business_name = (result['name']).lower()
            self.assertTrue(search_key in business_name)

    # @pytest.mark.run(order = 10)
    def test_users_retrieve_only_avail_business_info_and_reviews(self):
        raw_id = 1000000
        responses = [self.testHelper.get_business(raw_id),
                     self.testHelper.get_all_reviews(raw_id)]
        for resp in responses:
            res_msg = (json.loads(resp.data.decode("utf-8")))["msg"]
            # test message to match regex
            pattern = r"^UNSUCCESSFUL:.+$"
            self.assertRegexpMatches(res_msg, pattern)

    # @pytest.mark.run(order = 11)
    def test_users_can_update_business_info(self):
        raw_id = 1000
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.register_business(business_data, access_token)
        #update business
        self.testHelper.update_business(raw_id, update_data, access_token)
        # get the business's info in it's new state
        res = self.testHelper.get_business(raw_id)
        res_business_info = (json.loads(res.data.decode("utf-8")))["info"]

        for key, value in update_data.items():
            self.assertEqual(update_data[key], res_business_info[key])

    def test_only_logged_in_users_can_update_business(self):
        raw_id = 1000
        # try update without an access token
        resp = self.testHelper.update_business(raw_id, update_data)
        self.assertEqual(resp.status_code, 401)

    def test_users_cannot_update_with_existing_business_names(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.register_business(business_data, access_token)
        # register another businesses: business_data[1] has name Google
        self.testHelper.register_business(businesses_data[1], access_token)
        # try to update first business with name Google
        name_update_data = {"name": "Google"}
        resp = self.testHelper.update_business(1000, name_update_data, access_token)
        msg = (json.loads(resp.data.decode('utf-8')))['msg']
        self.assertEqual(msg, "Duplicate business name not allowed")


    def test_users_cannot_update_with_blank_names(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.register_business(business_data, access_token)
        # register another businesses: business_data[1] has name Google
        self.testHelper.register_business(businesses_data[1], access_token)
        # try to update first business with name Google
        name_update_data = {"name": "  "}
        resp = self.testHelper.update_business(1000, name_update_data, access_token)
        msg = (json.loads(resp.data.decode('utf-8')))['msg']
        self.assertEqual(msg, "Please provide name")


    def test_handles_updating_or_deleting_unavailble_business_id(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        # update with an unavailable id
        name_update_data = {"name": "Google"}
        responses = []
        responses.extend([
            # update unavailable business
            self.testHelper.update_business(10001, name_update_data, access_token),
            # del unavailable business
            self.testHelper.delete_business(10001, access_token)])
        for resp in responses:
            res_msg = (json.loads(resp.data.decode("utf-8")))["msg"]
            # test message to match regex
            pattern = r"^UNSUCCESSFUL:.+$"
            self.assertRegexpMatches(res_msg, pattern)

    # @pytest.mark.run(order = 13)
    def test_users_can_delete_business(self):
        self.testHelper.register_user(user_data)
        # login the first user
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.register_business(business_data, access_token)
        # delete business
        resp = self.testHelper.delete_business(1000, access_token)
        # count businesses with id = 1000
        db_count = self.db_object_count(Business, 'id', 1000)
        self.assertTrue(db_count == 0)
        #
        msg = (json.loads(resp.data.decode("utf-8")))["msg"]
        self.assertEqual(msg, "SUCCESS: business deleted")

    # @pytest.mark.run(order = 12)
    def test_users_can_only_update_or_delete_their_business(self):
        self.testHelper.register_user(user_data)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.register_business(business_data, access_token)
        # logout the current user
        self.testHelper.logout_user(access_token)
        # create a second user`
        self.testHelper.register_user(user_data2)
        res = self.testHelper.login_user(login_data2)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        # try to update and del a business created by the just logged out user
        responses = []
        responses.extend([
            # unauthorised update
            self.testHelper.update_business(1000, update_data, access_token),
            # unauthorised del
            self.testHelper.delete_business(1000, access_token)])
        for resp in responses:
            self.assertEqual(resp.status_code, 403)

    # @pytest.mark.run(order = 14)
    def test_users_can_make_a_review(self):
        self.testHelper.register_user(user_data)
        self.testHelper.register_user(user_data2)
        # login the first user
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.register_business(business_data, access_token)
        self.testHelper.logout_user(access_token)
        # login second user
        res = self.testHelper.login_user(login_data2)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        # second user make a review
        resp = self.testHelper.make_review(1000, review_data[0], access_token)
        # check count of review with sent heading in db
        posted_heading = review_data[0]['heading']
        db_count = self.db_object_count(Review, 'heading', posted_heading)
        self.assertEqual(db_count, 1)
        # test response message
        msg = (json.loads(resp.data.decode("utf-8")))["msg"]
        pattern = r"^SUCCESS:.+$"
        self.assertRegexpMatches(msg, pattern)
        self.testHelper.logout_user(access_token)

    # @pytest.mark.run(order = 15)
    def test_user_can_get_reviews(self):
        self.testHelper.register_user(user_data)
        self.testHelper.register_user(user_data2)
        res = self.testHelper.login_user(login_data)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.register_business(business_data, access_token)
        self.testHelper.make_review(1000, review_data[0], access_token)
        self.testHelper.logout_user(access_token)
        # login another user
        res = self.testHelper.login_user(login_data2)
        access_token = (json.loads(res.data.decode("utf-8")))['access_token']
        self.testHelper.make_review(1000, review_data[1], access_token)
        resp = self.testHelper.get_all_reviews(1000)
        reviews_info = (json.loads(resp.data.decode("utf-8")))['info']
        resp_review_headings = [review_info['heading']
                                for review_info in reviews_info]
        # check that all review heading have been returned
        for data in review_data:
            self.assertIn(data['heading'], resp_review_headings)

    def get_password_reset_link(self, username):
        self.testHelper.register_user(user_data)
        reset_data = {"username": username}
        resp = self.testHelper.reset_password(reset_data)
        reset_link = (json.loads(resp.data.decode('utf-8')))['reset_link']
        return reset_link

    def supply_new_password(self, reset_link, reset_data):
        resp = self.testHelper.reset_password_verify(reset_link, 'POST', reset_data)
        return resp

    def test_users_can_reset_passwords(self):
        # use username to send password reset request
        username = user_data['username']
        reset_link = self.get_password_reset_link(username)
        # client first clicks link within their email inbox to get update password form
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
            +fake_token
        resp = self.testHelper.reset_password_verify(fake_link, 'POST', reset_data)
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
