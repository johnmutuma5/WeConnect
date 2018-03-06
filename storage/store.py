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
        username = user_obj.username
        self.__class__.users[username] = user_obj
        new_user = self.__class__.users[username]
        return 'SUCCESS: user {} created!'.format(new_user.username)
