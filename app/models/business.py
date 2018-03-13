from app import store
from ..exceptions import InvalidUserInputError
import re

class Business ():
    '''
    Business template:
        methods:
            static:
                gen_id_string:
                    generates a valid business id given an integer
                    params: int::num
    '''
    business_count = 0


    @classmethod
    def create_business (cls, data, owner_id):
        cls.business_count = store.get_business_count ()
        new_business = cls (data, owner_id)
        new_business.mobile = data['mobile']
        new_business.id = cls.business_count + 1
        return new_business

    @staticmethod
    def gen_id_string (num):
        return 'BUS{:0>5}'.format(num)

    def __init__ (self, data, owner_id):
        self._id = None
        self._mobile = None
        self.name = data['name']
        self.owner_id = owner_id
        self.location = data ['location']

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
            raise InvalidUserInputError ("Business::mobile.setter", "Invalid mobile number")

    @property
    def id (self):
        return self._id

    @id.setter
    def id (self, id):
        '''generates an 8-character commnet id e.g. BUS00001
        '''
        self._id = 'BUS{:0>5}'.format(id)
        return
