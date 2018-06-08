
class CustomException (Exception):
    def __init__(self, expression=None, msg=None):
        self.expression = expression
        self.msg = msg


class DuplicationError (CustomException):
    '''
        raised: when storing duplicate data
    '''


class DataNotFoundError (CustomException):
    '''
        raised: when retrieving unavailable data
    '''


class PermissionDeniedError (CustomException):
    '''
        raised: when trying to read/write unauthorised data
    '''


class InvalidUserInputError (CustomException):
    '''
        raised: when trying to write invalid data
    '''

class UnknownPropertyError(CustomException):
    '''
        raised: when user uses invalid value for a class attribute
    '''


class MissingDataError(InvalidUserInputError):
    '''
        raised: when data passed by user lacks some required fields
    '''


class PaginationError(CustomException):
    '''
        raised: when user uses invalid page and limit values for pagination
    '''
