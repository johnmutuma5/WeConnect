from app import store

class Review ():
    '''
    Review
    Params: None
    '''

    review_count = store.get_review_count ()

    @classmethod
    def create_review (cls, business_id, author_id, data):
        return cls (business_id, author_id, data)

    @staticmethod
    def gen_id_string (num):
        return 'REV{:0>5}'.format(num)

    def __init__ (self,business_id, author_id, data):
        self.heading = data['heading']
        self.body = data['body']
        self.author_id = author_id
        self.business_id = business_id
        self._id = None
        self.id = self.__class__.review_count + 1 # a property set to a formated string

    @property
    def id (self):
        return self._id

    @id.setter
    def id (self, id):
        '''generates an 8-character commnet id e.g. REV00001
        '''
        self.__class__.review_count += 1
        self._id = 'REV{:0>5}'.format(id)
        return

    def handback_unused_id (self):
        self.__class__.review_count -= 1
