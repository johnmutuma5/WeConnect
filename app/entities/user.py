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
        self.contact = {"mobile": data['mobile'], "email": data['email']}
        self.password = data['password']
