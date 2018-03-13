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

    @staticmethod
    def extract_review_info (target_id, review):
        review_info = {}

        review_info["heading"] = review.heading
        review_info["body"] = review.body
        review_info["author_id"] = review.author_id
        review_info["business_id"] = review.business_id
        review_info["id"] = review.id

        return review_info

class Storage ():
    '''
    Simulates a database:
    Implemented with dicts for constant time access to data
        params: None
        fields:
            users: a dict of users (key:value) equivalent (username: user_obj)
            businesses: a dict o businesses (key:value) equivalent (businessname: business_obj)
            reviews: a dict o reviews (key:value) equivalent (reviewid: review_obj)
        methods:
            add: adds any class of object
                params: obj
            add_user:
                params: user_obj
            add_business:
                params: business_obj
            add_review:
                params: review_obj

    '''
    users = {}
    businesses = {}
    reviews = {}

    def __init__ (self):
        self.clerk = StoreHelper ()


    def add (self, obj):
        obj_class = obj.__class__.__name__

        # get appropriate method to call: a switch-like dict operation
        _add = {
            "User": self.add_user,
            "Business": self.add_business,
            "Review": self.add_review
        }[obj_class]

        # call method with argument and return it's output
        return _add (obj)

    def add_review (self, review_obj):
        review_id = review_obj.id
        self.__class__.reviews[review_id] = review_obj
        new_review = self.__class__.reviews[review_id]
        return 'SUCCESS: review heading:[{}] created!'.format(new_review.heading)


    def add_user (self, user_obj):
        users = self.__class__.users
        username = user_obj.username

        if users.get(username): raise DuplicationError ('Storage::add_user',
                                                        'Username already exists')

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

    def get_review_count (self):
        reviews = self.__class__.reviews
        return len(reviews)


    def get_businesses_info (self):
        businesses_info = []
        for business in self.__class__.businesses.values():
            business_data = self.clerk.extract_business_data (business)
            businesses_info.append (business_data)

        return businesses_info

    def find_by_id (self, _id, iterable_list):
        target_obj = None
        for obj in iterable_list:
            if obj.id == _id:
                target_obj = obj
        return target_obj

    def get_reviews_info (self, business_id):
        businesses = [business for business in self.__class__.businesses.values ()]
        target_business = self.find_by_id (business_id, businesses)
        reviews_info = []
        if target_business:
            target_id = target_business.id
            for review in self.__class__.reviews.values():
                if review.business_id == target_id:
                    review_info = self.clerk.extract_review_info (target_id, review)
                    reviews_info.append (review_info)

            return reviews_info
        msg = "UNSUCCESSFUL: Could not find the requested information"
        expression = "Storage::get_reviews_info ({})".format (business_id)
        raise DataNotFoundError (expression, msg)

    def get_business_info (self, business_id):
        businesses = [business for business in self.__class__.businesses.values ()]
        target_business = self.find_by_id (business_id, businesses)

        if target_business:
            business_info = self.clerk.extract_business_data (target_business)
            return business_info

        msg = "UNSUCCESSFUL: Could not find the requested information"
        expression = "Storage::get_business_info ({})".format (business_id)
        raise DataNotFoundError (expression, msg)

    def update_business (self, business_id, update_data, issuer_id):
        new_name = update_data.get ('name')
        if new_name:
            print (new_name)
            if self.__class__.businesses.get (new_name):
                raise DuplicationError ("Storage::update_business",
                                        'Duplicate business name not allowed')

        businesses = [business for business in self.__class__.businesses.values ()]
        target_business = self.find_by_id (business_id, businesses)

        if target_business:
            issuer_is_owner = target_business.owner_id == issuer_id
            if issuer_is_owner:
                old_key = target_business.name
                self.clerk.update_business (target_business, update_data)
                if new_name:
                    self.__class__.businesses[new_name] = target_business
                    del self.__class__.businesses[old_key]
                return "Changes recorded successfully"
            # if instruction issuer is not owner
            msg = "UNSUCCESSFUL: The business is registered to another user"
            expression = "Storage::get_business_info ({}, {})".format (business_id, issuer_id)
            raise PermissionDeniedError (expression, msg)
        # if a business with the business_id is not found
        msg = "UNSUCCESSFUL: Could not find the requested information"
        expression = "Storage::get_business_info ({})".format (business_id)
        raise DataNotFoundError (expression, msg)

    def delete_business (self, business_id, issuer_id):
        businesses = [business for business in self.__class__.businesses.values ()]
        target_business = self.find_by_id (business_id, businesses)
        if target_business:
            issuer_is_owner = target_business.owner_id == issuer_id
            if issuer_is_owner:
                # delete the business
                key = target_business.name
                del self.__class__.businesses[key]
                return "SUCCESS: business deleted"

            msg = "UNSUCCESSFUL: The business is registered to another user"
            expression = "Storage::delete_business ({}, {})".format(business_id, issuer_id)
            raise PermissionDeniedError (expression, msg)

        msg = "UNSUCCESSFUL: Could not find the requested information"
        expression = "Storage::delete_business ({}, {})".format(business_id, issuer_id)
        raise DataNotFoundError (expression, msg)


    def clear (self):
        self.__class__.users.clear ()
        self.__class__.businesses.clear ()
        return 'cleared'
