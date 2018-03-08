class DuplicationError (Exception):
    '''
        class: DuplicationError
        raised: when storing duplicate data
    '''
    def __init__ (self, expression, msg):
        self.expression = expression
        self.msg = msg


class DataNotFoundError (Exception):
    '''
        class: DuplicationError
        raised: when storing duplicate data
    '''
    def __init__ (self, expression, msg):
        self.expression = expression
        self.msg = msg
    
