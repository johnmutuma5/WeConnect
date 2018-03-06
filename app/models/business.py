class Business ():
    '''
    Business template
    '''

    @classmethod
    def create_business (cls, data):
        return cls (data)

    def __init__ (self, data):
        self.name = data['name']
        self.owner = data['owner']
        self.location = data ['location']
        self._mobile = data['mobile']

    @property
    def mobile (self):
        return self._mobile

    @mobile.setter
    def mobile (self, num):
        # should raise ValueError with invalid chars in mobille numbers
        num = int(num)
        self._mobile = num
