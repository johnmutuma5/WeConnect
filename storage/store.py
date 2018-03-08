from app.exceptions import DuplicationError


class Storage ():
    '''
    Simulates a database:
    Implemented with dicts for constant time access to data
        params: None
        fields:
            users: a dict of users (key:value) equivalent (username: user_obj)
            businesses: a dict o businesses (key:value) equivalent (businessname: business_obj)
        methods:
            add: adds any class of object
                params: obj
            add_user:
                params: user_obj
            add_business:
                params: business_obj

    '''
    users = {}
    businesses = {}

    def __init__ (self):
        ...

    def add (self, obj):
        obj_class = obj.__class__.__name__

        # get appropriate method to call: a switch-like dict operation
        _add = {
            "User": self.add_user,
            "Business": self.add_business
        }[obj_class]

        # call method with argument and return it's output
        return _add (obj)

    def add_user (self, user_obj):
        users = self.__class__.users
        username = user_obj.username

        if users.get(username): raise DuplicationError ('Storage::add_user',
                                                        'Duplicate username not allowed')

        self.__class__.users[username] = user_obj
        new_user = self.__class__.users[username]
        return 'SUCCESS: user {} created!'.format(new_user.username)

    def add_business (self, business_obj):
        businesses = self.__class__.businesses
        businessname = business_obj.name

        if businesses.get(businessname): raise DuplicationError ('Storage::add_business',
                                                                    'Duplicate business name not allowed')

        self.__class__.businesses[businessname] = business_obj
        new_business = self.__class__.businesses[businessname]
        return 'SUCCESS: business {} created!'.format(new_business.name)

    def get_business_count (self):
        businesses = self.__class__.businesses
        return len(businesses)

    def get_businesses_info (self):
        businesses_info = []
        for business in self.__class__.businesses.values():
            business_data = {}

            business_data["name"] = business.name
            business_data["owner"] = business.owner
            business_data["location"] = business.location
            business_data["mobile"] = business.mobile
            business_data["id"] = business.id

            businesses_info.append (business_data)
        return businesses_info

    def clear (self):
        self.__class__.users.clear ()
        self.__class__.businesses.clear ()
        return 'cleared'
