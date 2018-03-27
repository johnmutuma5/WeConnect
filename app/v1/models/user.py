from ..storage import store
from ...exceptions import InvalidUserInputError
import re

class User ():
    '''
    '''
    user_index = 0

    @classmethod
    def create_user (cls, data):
        cls.user_index = store.get_user_index ()
        new_user = cls (data)
        # assign to property fields
        new_user.id = cls.user_index + 1
        new_user.username = data['username']
        new_user.mobile = data['mobile']
        return new_user

    def __init__ (self, data):
        # self.first_name = data['first_name']
        # self.last_name = data['last_name']
        # self.gender = data['gender']
        # self.email = data['email']
        self._mobile = None
        self._id = None
        self._username = None
        self.password = data['password']

    @property
    def mobile (self):
        return self._mobile

    @mobile.setter
    def mobile (self, num):
        # should raise InvalidUserInputError with invalid chars in mobille numbers
        pattern = r"^[0-9]{12}$"
        match = re.match (pattern, num)
        if match:
            self._mobile = num
        else:
            raise InvalidUserInputError ("User::mobile.setter", "Invalid mobile number")

    # user id property
    @property
    def id (self):
        return self._id

    @id.setter
    def id (self, id):
        '''generates an 8-character commnet id e.g. USR00001
        '''
        # self.__class__.user_count += 1
        self._id = 'USR{:0>5}'.format(id)
        return

    @property
    def username (self):
        return self._username

    @username.setter
    def username (self, name):
        pattern = r'^[a-zA-Z_]+[\d\w]{3,}'
        match = re.search (pattern, name)
        if match:
            self._username = name
            return
        self._username = None
        # assert 0, 'Invalid username'
        raise InvalidUserInputError ("User::namesetter", "Invalid username!")

    def handback_unused_id (self):
        # self.__class__.user_count -= 1
        pass
