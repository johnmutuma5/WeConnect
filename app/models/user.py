from app import store
import re

class User ():
    '''
    '''
    user_count = store.get_user_count ()

    @classmethod
    def create_user (cls, data):
        return cls(data)

    def __init__ (self, data):
        # self.first_name = data['first_name']
        # self.last_name = data['last_name']
        # self.gender = data['gender']
        # self._mobile = None
        # self.mobile = data['mobile']
        # self.email = data['email']
        self._id = None
        self.id = self.__class__.user_count + 1
        self._username = None
        self.username = data['username']
        self.password = data['password']

    @property
    def mobile (self):
        return self._mobile

    @mobile.setter
    def mobile (self, num):
        # should raise ValueError for non-int characters
        num = int(num)
        self._mobile = num

    # user id property
    @property
    def id (self):
        return self._id

    @id.setter
    def id (self, id):
        '''generates an 8-character commnet id e.g. USR00001
        '''
        self.__class__.user_count += 1
        self._id = 'USR{:0>5}'.format(id)
        return

    @property
    def username (self):
        return self._username

    @username.setter
    def username (self, name):
        pattern = r'\w+'
        match = re.search (pattern, name)
        if match:
            self._username = name
            return
        self._username = None
        assert 0, 'Invalid username'

    def handback_unused_id (self):
        self.__class__.user_count -= 1
