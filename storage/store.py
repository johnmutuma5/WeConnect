from app.exceptions import DuplicationError

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
        users = self.__class__.users
        username = user_obj.username

        if users.get(username): raise DuplicationError ('Storage::add_user', 'Duplicates username not allowed')

        self.__class__.users[username] = user_obj
        new_user = self.__class__.users[username]
        return 'SUCCESS: user {} created!'.format(new_user.username)
