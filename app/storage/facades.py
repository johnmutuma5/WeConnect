import re
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import sessionmaker, scoped_session
from .base import weconnect_table_names
from app import config
from app.user.models import User, PasswordResetToken
from app.business.models import Business, Review
from app.user.schemas import REQUIRED_USER_FIELDS, USER_SEQUENCES
from app.business.schemas import(VALID_BUSINESS_FIELDS, REQUIRED_REVIEW_FIELDS,
                                 USER_DEFINED_BUSINESS_FIELDS, BUSINESS_SEQUENCES)
from app.exceptions import (DuplicationError, DataNotFoundError,
                            PermissionDeniedError, PaginationError,
                            UnknownPropertyError)


class StoreHelper ():
    '''Used to create a clerical helper for the DbInterface:
        Methods: extract_business_data
                update_business
                extract_review_info
    '''

    def __init__(self):
        ...

    @staticmethod
    def get_profile(_object, profile_type=None):
        return _object.profile(profile_type)

    @staticmethod
    def extract_business_data(business, session=None):
        business_data = {}
        fields = ["name", *VALID_BUSINESS_FIELDS, "id"]
        for field in fields:
            value = getattr(business, field)
            if isinstance(value, User):
                value = value.id
            business_data[field] = value
        return business_data

    @staticmethod
    def update_business(target_business, update_data):
        for key in update_data.keys():
            if key not in USER_DEFINED_BUSINESS_FIELDS:
                raise UnknownPropertyError(msg="Unknown property %s" %key)
            setattr(target_business, key, update_data[key])

    @staticmethod
    def extract_review_info(review):
        review_info = {}
        fields = [*REQUIRED_REVIEW_FIELDS, "id"]
        for field in fields:
            review_info[field] = getattr(review, field)

        return review_info


class DbFacade():

    def __init__(self, dbEngine):
        self.engine = dbEngine
        self.Session = scoped_session(sessionmaker(bind=dbEngine))
        self.clerk = StoreHelper()

    def add(self, obj):
        obj_class = obj.__class__.__name__

        # get appropriate method to call: a switch-like dict operation
        if obj_class == 'User':
            _add = self.add_user
        elif obj_class == 'Business':
            _add = self.add_business
        elif obj_class == "Review":
            _add = self.add_review

        # call method with argument and return it's output
        return _add(obj)

    def retrieve_field_raising_integrity_error(self, e):
        # see NAMING_CONVENTION in config
        pattern = config.get('NAMING_CONVENTION_REGEX')
        match = re.search(pattern, e.args[0])
        key = match.group('column')
        return key.capitalize()

    @staticmethod
    def handle_data_not_found(session=None):
        if session:
            session.close()
        msg = "UNSUCCESSFUL: Could not find the requested business"
        expression = "Storage::unavailable info"
        raise DataNotFoundError(expression, msg)

    @staticmethod
    def handle_permission_denied(session=None):
        if session:
            session.close()
        msg = "UNSUCCESSFUL: The business is registered to another user"
        expression = "Storage::unauthorised operation"
        raise PermissionDeniedError(expression, msg)


    def _process_results(self, results):
        results_info = []
        for business in results:
            business_info = self.clerk.extract_business_data(business)
            results_info.append(business_info)
        return results_info


    def _apply_pagination(self, limit=None, page=1, subquery=None):
        try:
            limit = int(limit)
            offset = limit * (int(page) - 1)
            subquery = subquery.limit(limit).offset(offset)
        except (ValueError, TypeError):
            raise PaginationError(msg="Invalid pagination limit or page")

        return subquery


    def _revert_sequence_increment(self, sequence=None, table_name=None):
        '''Reverts auto increment of sequences after failed database insertions'''
        all_tables = weconnect_table_names()

        if table_name in all_tables:
            sql = "SELECT SETVAL(:seq, (SELECT MAX(id) from %s))"%(table_name,)

        bind_params = {'seq': sequence}
        session = self.Session()
        session.execute(sql, bind_params)
        # scoped session is closed at the parent scope



class BusinessDbFacade(DbFacade):

    def add_business(self, business_obj):
        businessname = business_obj.name
        session = self.Session()
        try:
            session.add(business_obj)
            session.commit()
        except IntegrityError:
            session.rollback()
            # revert the database sequence auto increment
            seq = BUSINESS_SEQUENCES.get('business')
            self._revert_sequence_increment(sequence=seq,
                                            table_name='business')
            raise DuplicationError('Storage::add_business',
                                   'Business name already exists')
        finally:
            session.close()
        return 'SUCCESS: business {} created!'.format(businessname)


    def get_businesses_info(self):
        businesses_info = []
        session = self.Session()
        businesses = session.query(Business).all()
        for business in businesses:
            business_data = self.clerk.extract_business_data(business, session)
            businesses_info.append(business_data)
        session.close()
        return businesses_info


    def get_business_info(self, business_id):
        session = self.Session()
        target_business = session.query(Business)\
            .filter(Business.id == business_id)\
            .first()
        try:
            if not target_business:
                self.handle_data_not_found()
            # session.expunge (target_business)
            business_info = self.clerk.extract_business_data(target_business)
            return business_info
        finally:
            session.close()


    def search_businesses(self, search_params):
        session = self.Session()
        search_key = search_params.get('q', '')

        _operator = '%' + search_key + '%'
        subquery = session.query(Business)\
            .filter(Business.name.ilike(_operator))

        # pagination
        limit = search_params.get('limit', 10)
        page = search_params.get('page', 1)
        subquery = self._apply_pagination(limit, page, subquery)
        results = subquery.all()

        results_info = self._process_results(results)
        session.close()
        return results_info


    def filter_businesses(self, filter_params):
        session = self.Session()
        subquery = session.query(Business)
        for key in filter_params.keys():
            if key not in VALID_BUSINESS_FIELDS:
                continue
            search_key = filter_params[key]
            _operator = '%' + search_key + '%'
            subquery = subquery.filter(getattr(Business, key).ilike(_operator))

        # pagination
        limit = filter_params.get("limit", 10)
        page = filter_params.get("page", 1)
        subquery = self._apply_pagination(limit, page, subquery)
        results = subquery.all()

        results_info = self._process_results(results)
        session.close()
        return results_info


    def update_business(self, business_id, update_data, issuer_id):
        session = self.Session()
        target_business = session.query(Business)\
            .filter(Business.id == business_id)\
            .first()
        # check if target_business exists
        if not target_business:
            return self.handle_data_not_found(session)
        # check if request issuer is owner
        issuer_is_owner = target_business.owner_id == issuer_id
        if not issuer_is_owner:
            return self.handle_permission_denied(session)
        # except updating with an existent name
        try:
            self.clerk.update_business(target_business, update_data)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise DuplicationError("Storage::update_business",
                                   'Duplicate business name not allowed')
        finally:
            session.close()
        # everything is okay
        return "Changes recorded successfully"


    def delete_business(self, business_id, issuer_id):
        session = self.Session()
        target_business = session.query(Business)\
            .filter(Business.id == business_id)\
            .first()

        # if business with id = business_id is not found
        if not target_business:
            self.handle_data_not_found(session)

        # check if request issuer is owner
        issuer_is_owner = target_business.owner_id == issuer_id
        if not issuer_is_owner:
            self.handle_permission_denied(session)

        # everything is okay, delete the business
        session.delete(target_business)
        session.commit()
        return "SUCCESS: business deleted"


    def add_review(self, review_obj):
        session = self.Session()
        try:
            session.add(review_obj)
            session.commit()
        except IntegrityError:
            session.rollback()
            # revert the database sequence auto increment
            seq = BUSINESS_SEQUENCES.get('review')
            self._revert_sequence_increment(sequence=seq,
                                            table_name='review')
            return self.handle_data_not_found()
        finally:
            session.close()
        return 'SUCCESS: review posted!'


    def get_reviews_info(self, business_id):
        session = self.Session()
        target_business = session.query(Business)\
            .filter(Business.id == business_id)\
            .first()

        # if business with id business_id is not found
        if not target_business:
            self.handle_data_not_found(session)

        target_reviews = session.query(Review)\
            .filter(Review.business_id == business_id)\
            .all()

        reviews_info = []
        for review in target_reviews:
            # session.expunge(review)
            review_info = self.clerk.extract_review_info(review)
            reviews_info.append(review_info)
        session.close()
        return reviews_info


class UserDbFacade(DbFacade):

    def add_user(self, user_obj):
        session = self.Session()
        username = user_obj.username
        try:
            session.add(user_obj)
            session.commit()
        except (IntegrityError) as e:
            key = self.retrieve_field_raising_integrity_error(e)
            session.rollback()
            # revert the database sequence auto increment
            seq = USER_SEQUENCES.get('users')
            self._revert_sequence_increment(sequence=seq,
                                            table_name='users')
            raise DuplicationError('Storage::add_user',
                                   '%s already exists' % key)
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


    def get_user_profile(self, user_id, profile_type=None):
        session = self.Session()
        target_user = session.query(User)\
            .filter(User.id == user_id)\
            .first()
        profile = self.clerk.get_profile(target_user, profile_type)
        session.close()
        return profile


    def add_token(self, token_obj, bearer_name):
        session = self.Session()
        session.add(token_obj)
        session.commit()

    def get_token_tuple(self, token_string):
        session = self.Session()
        token_obj = session.query(PasswordResetToken)\
            .filter(PasswordResetToken.token_string == token_string)\
            .first()
        bearer = None
        if token_obj:
            bearer = token_obj.bearer
        session.close()
        return token_obj, bearer

    def destroy_token(self, token_obj):
        session = self.Session()
        session.delete(token_obj)
        session.commit()

    def update_user_password(self, token_bearer, new_password):
        session = self.Session()
        token_bearer.password = new_password
        target_user = session.query(User)\
            .filter(User.username == token_bearer.username)\
            .first()
        target_user.password = new_password
        session.commit()
