class Storage ():
    '''
    Simulates a database:
        params: None
        fields:
            users: a dict of users (key:value) equivalent (username: user)
        methods:
            add_user:
                params: user_obj

    '''
    users = {}

    def __init__ (self):
        ...

    def add_user (self, user_obj):
        self.__class__.users['username'] = user_obj
