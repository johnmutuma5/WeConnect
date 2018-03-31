from ...exceptions import DuplicationError, DataNotFoundError, PermissionDeniedError
from app.v2.models import User, Business, Review, Token
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import sessionmaker


class StoreHelper ():
    '''Used to create a clerical helper for the DbInterface:
        Methods: extract_business_data
                update_business
                extract_review_info
    '''

    def __init__(self):
        ...

    @staticmethod
    def extract_business_data(business):
        business_data = {}
        fields = ["name", "owner_id", "location", "mobile", "id"]
        for field in fields:
            business_data[field] = getattr(business, field)

        return business_data

    @staticmethod
    def update_business(target_business, update_data):
        for key in update_data.keys():
            setattr(target_business, key, update_data[key])

    @staticmethod
    def extract_review_info(review):
        review_info = {}
        fields = ["heading", "body", "author_id", "business_id", "id"]
        for field in fields:
            review_info[field] = getattr(review, field)

        return review_info


class DbInterface ():

    def __init__(self, dbEngine):
        self.engine = dbEngine
        self.Session = sessionmaker(bind=dbEngine)
        self.clerk = StoreHelper()

    def add(self, obj):
        obj_class = obj.__class__.__name__

        # get appropriate method to call: a switch-like dict operation
        _add = {
            "User": self.add_user,
            "Business": self.add_business,
            "Review": self.add_review
        }[obj_class]

        # call method with argument and return it's output
        return _add(obj)

    def add_user(self, user_obj):
        session = self.Session()
        username = user_obj.username
        try:
            session.add(user_obj)
            session.commit()
        except (IntegrityError):
            session.rollback()
            raise DuplicationError('Storage::add_user',
                                   'Username already exists')
        finally:
            session.close()

        return 'SUCCESS: user {} created!'.format(username)

    def get_user(self, username):
        session = self.Session()
        target_user = session.query(User)\
            .filter(User.username == username)\
            .first()
        session.close()
        return target_user

    def add_business(self, business_obj):
        businessname = business_obj.name
        session = self.Session()
        try:
            session.add(business_obj)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise DuplicationError('Storage::add_business',
                                   'Business name already exists')
        finally:
            session.close()
        return 'SUCCESS: business {} created!'.format(businessname)

    def get_businesses_info(self):
        businesses_info = []
        session = self.Session()
        businesses = session.query(Business).all()
        session.close()
        for business in businesses:
            business_data = self.clerk.extract_business_data(business)
            businesses_info.append(business_data)
        return businesses_info

    def handle_data_not_found(self, session=None):
        if session:
            session.close()
        msg = "UNSUCCESSFUL: Could not find the requested information"
        expression = "Storage::unavailable info"
        raise DataNotFoundError(expression, msg)

    def handle_permission_denied(self, session=None):
        if session:
            session.close()
        msg = "UNSUCCESSFUL: The business is registered to another user"
        expression = "Storage::unauthorised operation"
        raise PermissionDeniedError(expression, msg)

    def get_business_info(self, business_id):
        session = self.Session()
        target_business = session.query(Business)\
            .filter(Business.id == business_id)\
            .first()
        session.close()
        if target_business:
            # session.expunge (target_business)
            business_info = self.clerk.extract_business_data(target_business)
            return business_info
        self.handle_data_not_found()

    def update_business(self, business_id, update_data, issuer_id):
        session = self.Session()
        target_business = session.query(Business)\
            .filter(Business.id == business_id)\
            .first()
        if target_business:
            issuer_is_owner = target_business.owner_id == issuer_id
            if issuer_is_owner:
                try:
                    self.clerk.update_business(target_business, update_data)
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    raise DuplicationError("Storage::update_business",
                                           'Duplicate business name not allowed')
                finally:
                    session.close()
                return "Changes recorded successfully"
            # if instruction issuer is not owner
            self.handle_permission_denied(session)
        # if a business with the business_id is not found
        self.handle_data_not_found(session)

    def delete_business(self, business_id, issuer_id):
        session = self.Session()
        target_business = session.query(Business)\
            .filter(Business.id == business_id)\
            .first()
        if target_business:
            issuer_is_owner = target_business.owner_id == issuer_id
            if issuer_is_owner:
                # delete the business
                session.delete(target_business)
                session.commit()
                return "SUCCESS: business deleted"
            # if issuer is not owner
            self.handle_permission_denied(session)
        # if business with id = business_id is not found
        self.handle_data_not_found(session)

    def add_review(self, review_obj):
        session = self.Session()
        session.add(review_obj)
        session.commit()
        return 'SUCCESS: review posted!'

    def get_reviews_info(self, business_id):
        session = self.Session()
        target_business = session.query(Business)\
            .filter(Business.id == business_id)\
            .first()
        if target_business:
            target_reviews = session.query(Review)\
                .filter(Review.business_id == business_id)\
                .all()
            reviews_info = []
            if len(target_reviews) > 0:
                for review in target_reviews:
                    session.expunge(review)
                    review_info = self.clerk.extract_review_info(review)
                    reviews_info.append(review_info)
            session.close()
            return reviews_info
        # if business with id business_id is not found
        self.handle_data_not_found(session)

    def add_token(self, token_obj, bearer_name):
        session = self.Session()
        session.add(token_obj)
        session.commit()

    def get_token_tuple(self, token_string):
        session = self.Session()
        token_obj = session.query(Token)\
            .filter(Token.token_string == token_string)\
            .first()
        bearer = None
        if token_obj:
            bearer = token_obj.bearer
        session.close()
        return token_obj, bearer

    def destroy_token(self, token_obj):
        session = self.Session()
        # target_token = session.query(Token)\
        #     .filter(Token.token_string)
        session.delete(token_obj)
        session.commit()

    def update_user_password(self, token_bearer, new_password):
        session = self.Session()
        token_bearer.password = new_password
        j = session.query(User)\
            .filter(User.username == token_bearer.username)\
            .first()
        j.password = new_password
        session.commit()

# class Storage ():
#     '''
#     Simulates a database:
#     Implemented with dicts for constant time access to data
#         params: None
#         fields:
#             users: a dict of users (key:value) equivalent (username: user_obj)
#             businesses: a dict o businesses (key:value) equivalent (businessname: business_obj)
#             reviews: a dict o reviews (key:value) equivalent (reviewid: review_obj)
#             tokens: a dict of tokens (key:value) equivalent (token_string: bearer_name)
#         methods:
#             add: adds any class of object
#                 params: obj
#             add_user:
#                 params: user_obj
#             add_business:
#                 params: business_obj
#             add_review:
#                 params: review_obj
#
#     '''
#     users = {}
#     businesses = {}
#     reviews = {}
#     counts = {
#         'users': 0,
#         'businesses': 0,
#         'reviews': 0
#     }
#     tokens = {}
#
#     def __init__ (self):
#         self.clerk = StoreHelper ()
#
#
#     def add (self, obj):
#         obj_class = obj.__class__.__name__
#
#         # get appropriate method to call: a switch-like dict operation
#         _add = {
#             "User": self.add_user,
#             "Business": self.add_business,
#             "Review": self.add_review
#         }[obj_class]
#
#         # call method with argument and return it's output
#         return _add (obj)
#
#     def add_review (self, review_obj):
#         review_id = review_obj.id
#         self.__class__.reviews[review_id] = review_obj
#         # increment count of reviews ever stored
#         self.__class__.counts['reviews'] += 1
#         new_review = self.__class__.reviews[review_id]
#         return 'SUCCESS: review heading:[{}] created!'.format(new_review.heading)
#
#
#     def add_user (self, user_obj):
#         users = self.__class__.users
#         username = user_obj.username
#
#         if users.get(username): raise DuplicationError ('Storage::add_user',
#                                                         'Username already exists')
#
#         self.__class__.users[username] = user_obj
#         # increment the cont of users ever stored
#         self.__class__.counts['users'] += 1
#         new_user = self.__class__.users[username]
#         return 'SUCCESS: user {} created!'.format(new_user.username)
#
#
#     def add_business (self, business_obj):
#         businesses = self.__class__.businesses
#         businessname = business_obj.name
#
#         if businesses.get(businessname): raise DuplicationError ('Storage::add_business',
#                                                                     'Duplicate business name not allowed')
#
#         self.__class__.businesses[businessname] = business_obj
#         # increment the count of businesses ever stored
#         self.__class__.counts['businesses'] += 1
#         new_business = self.__class__.businesses[businessname]
#         return 'SUCCESS: business {} created!'.format(new_business.name)
#
#     def add_token (self, token, bearer_name):
#         self.__class__.tokens [token] = bearer_name
#
#     def get_business_index (self):
#         index = self.__class__.counts['businesses']
#         return index
#
#     def get_user_index (self):
#         index = self.__class__.counts['users']
#         return index
#
#     def get_review_index (self):
#         index = self.__class__.counts['reviews']
#         return index
#
#
#     def get_businesses_info (self):
#         businesses_info = []
#         for business in self.__class__.businesses.values():
#             business_data = self.clerk.extract_business_data (business)
#             businesses_info.append (business_data)
#
#         return businesses_info
#
#     def find_by_id (self, _id, iterable_list):
#         target_obj = None
#         for obj in iterable_list:
#             if obj.id == _id:
#                 target_obj = obj
#         return target_obj
#
#     def get_reviews_info (self, business_id):
#         businesses = [business for business in self.__class__.businesses.values ()]
#         target_business = self.find_by_id (business_id, businesses)
#         reviews_info = []
#         if target_business:
#             target_id = target_business.id
#             for review in self.__class__.reviews.values():
#                 if review.business_id == target_id:
#                     review_info = self.clerk.extract_review_info (review)
#                     reviews_info.append (review_info)
#
#             return reviews_info
#         msg = "UNSUCCESSFUL: Could not find the requested information"
#         expression = "Storage::get_reviews_info ({})".format (business_id)
#         raise DataNotFoundError (expression, msg)
#
#     def get_business_info (self, business_id):
#         businesses = [business for business in self.__class__.businesses.values ()]
#         target_business = self.find_by_id (business_id, businesses)
#
#         if target_business:
#             business_info = self.clerk.extract_business_data (target_business)
#             return business_info
#
#         msg = "UNSUCCESSFUL: Could not find the requested information"
#         expression = "Storage::get_business_info ({})".format (business_id)
#         raise DataNotFoundError (expression, msg)
#
#     def update_business (self, business_id, update_data, issuer_id):
#         new_name = update_data.get ('name')
#         if new_name:
#             if self.__class__.businesses.get (new_name):
#                 raise DuplicationError ("Storage::update_business",
#                                         'Duplicate business name not allowed')
#
#         businesses = [business for business in self.__class__.businesses.values ()]
#         target_business = self.find_by_id (business_id, businesses)
#
#         if target_business:
#             issuer_is_owner = target_business.owner_id == issuer_id
#             if issuer_is_owner:
#                 old_key = target_business.name
#                 self.clerk.update_business (target_business, update_data)
#                 if new_name:
#                     self.__class__.businesses[new_name] = target_business
#                     del self.__class__.businesses[old_key]
#                 return "Changes recorded successfully"
#             # if instruction issuer is not owner
#             msg = "UNSUCCESSFUL: The business is registered to another user"
#             expression = "Storage::get_business_info ({}, {})".format (business_id, issuer_id)
#             raise PermissionDeniedError (expression, msg)
#         # if a business with the business_id is not found
#         msg = "UNSUCCESSFUL: Could not find the requested information"
#         expression = "Storage::get_business_info ({})".format (business_id)
#         raise DataNotFoundError (expression, msg)
#
#     def delete_business (self, business_id, issuer_id):
#         businesses = [business for business in self.__class__.businesses.values ()]
#         target_business = self.find_by_id (business_id, businesses)
#         if target_business:
#             issuer_is_owner = target_business.owner_id == issuer_id
#             if issuer_is_owner:
#                 # delete the business
#                 key = target_business.name
#                 del self.__class__.businesses[key]
#                 return "SUCCESS: business deleted"
#
#             msg = "UNSUCCESSFUL: The business is registered to another user"
#             expression = "Storage::delete_business ({}, {})".format(business_id, issuer_id)
#             raise PermissionDeniedError (expression, msg)
#
#         msg = "UNSUCCESSFUL: Could not find the requested information"
#         expression = "Storage::delete_business ({}, {})".format(business_id, issuer_id)
#         raise DataNotFoundError (expression, msg)
#
#
#     def clear (self):
#         self.__class__.users.clear ()
#         self.__class__.businesses.clear ()
#         self.__class__.reviews.clear ()
#         self.__class__.counts['users'] = 0
#         self.__class__.counts['businesses'] = 0
#         self.__class__.counts['reviews'] = 0
#         return 'cleared'
