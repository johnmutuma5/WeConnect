class Review ():
    '''
    Review
    Params: None
    '''
    @classmethod
    def creat_review (cls, data):
        return cls (data)

    def __init__ (self, data):
        self.author = data['author']
        self.message = data['message']
        self.business = data['business']
    
