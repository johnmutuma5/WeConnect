from app import store

class Business ():
    '''
    Business template:
        methods:
            static:
                gen_id_string:
                    generates a valid business id given an integer
                    params: int::num
    '''
    business_count = store.get_business_count ()


    @classmethod
    def create_business (cls, data):
        return cls (data)

    @staticmethod
    def gen_id_string (num):
        return 'BUS{:0>5}'.format(num)

    def __init__ (self, data):
        self._id = None
        self._mobile = data['mobile']
        self.id = self.__class__.business_count + 1 # a property set to a formated string
        self.name = data['name']
        self.owner = data['owner']
        self.location = data ['location']

    @property
    def mobile (self):
        return self._mobile

    @mobile.setter
    def mobile (self, num):
        # should raise ValueError with invalid chars in mobille numbers
        num = int(num)
        self._mobile = num

    @property
    def id (self):
        return self._id

    @id.setter
    def id (self, id):
        '''generates an 8-character commnet id e.g. BUS00001
        '''
        self.__class__.business_count += 1
        self._id = 'BUS{:0>5}'.format(id)
        return



    def handback_unused_id (self):
        self.__class__.business_count -= 1
