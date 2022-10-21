"""
"""


class User:
    def __init__(self, id):
        self._id = id

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self._id
    
    @property
    def name(self):
        return self._id
