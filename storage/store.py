from app.exceptions import DuplicationError, DataNotFoundError, PermissionDeniedError
class StoreHelper ():
    def __init__ (self):
        ...

    @staticmethod
    def extract_business_data (business):
        business_data = {}

        business_data["name"] = business.name
        business_data["owner_id"] = business.owner_id
        business_data["location"] = business.location
        business_data["mobile"] = business.mobile
        business_data["id"] = business.id

        return business_data

    @staticmethod
    def update_business (target_business, update_data):
        for key, value in update_data.items ():
            setattr(target_business, key, update_data[key])


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
        self.clerk = StoreHelper ()


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

    def get_user_count (self):
        users = self.__class__.users
        return len(users)


    def get_businesses_info (self):
        businesses_info = []
        for business in self.__class__.businesses.values():
            business_data = self.clerk.extract_business_data (business)
            businesses_info.append (business_data)

        return businesses_info


    def get_business_info (self, business_id):
        businesses = [business for business in self.__class__.businesses.values ()]
        target_business = None
        for business in businesses:
            if business.id == business_id:
                target_business = business
        if target_business:
            business_info = self.clerk.extract_business_data (target_business)
            return business_info

        msg = "UNSUCCESSFUL: Could not find the requested information"
        expression = "Storage::get_business_info ({})".format (business_id)
        raise DataNotFoundError (expression, msg)

    def update_business (self, business_id, update_data, issuer_id):
        businesses = [business for business in self.__class__.businesses.values ()]
        target_business = None
        for business in businesses:
            if business.id == business_id:
                target_business = business

        issuer_is_owner = target_business.owner_id == issuer_id
        if target_business:
            if issuer_is_owner:
                self.clerk.update_business (target_business, update_data)
                return "Changes recorded successfully"
            msg = "UNSUCCESSFUL: The business is registered to another user"
            expression = "Storage::get_business_info ({}, {})".format (business_id, issuer_id)
            raise PermissionDeniedError (expression, msg)

        msg = "UNSUCCESSFUL: Could not find the requested information"
        expression = "Storage::get_business_info ({})".format (business_id)
        raise DataNotFoundError (expression, msg)

    def clear (self):
        self.__class__.users.clear ()
        self.__class__.businesses.clear ()
        return 'cleared'
