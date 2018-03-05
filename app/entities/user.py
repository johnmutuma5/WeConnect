class User ():
    '''
    '''
    @classmethod
    def create_user (cls, data):
        return cls(data)

    def __init__ (self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.gender = data['gender']
        self._mobile = data['mobile']
        self.email = data['email']
        self.password = data['password']

    @property
    def mobile (self):
        return self._mobile

    @mobile.setter
    def mobile (self, num):
        # should raise ValueError for non-int characters
        num = int(num)
        self._mobile = num
