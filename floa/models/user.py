from floa.extensions import db
from floa.models.library import Library
from flask_login import UserMixin

class User(UserMixin):
    ''' User object

        id: private member for database record key
        uid: UUID for use in browser cookie and session to allow session 
             invalidation
    '''
    def __init__(self, id, name, email, library, created_date, alt_id=None):
        self._id = id
        self.name = name
        self.email = email
        self.library = library
        self.created_date = created_date
        self.uid = None

    @staticmethod
    def init(record):
        user = User(
            id=record.get('id'),
            name=record.get('name'),
            email=record.get('email'),
            library=Library(library=record.get('library')),
            created_date=record.get('created_date'),
            alt_id=record.get('alt_id')
        )  
        return user

    @staticmethod
    def get(user_id):
        ''' user_id == uid '''
        user = None
        record = db.get_user_by_alt_id(user_id)
        if record:
            user = User.init(record)
        return user

    @staticmethod
    def new(name, email):
        record = db.create(name, email)
        return User.init(record)
