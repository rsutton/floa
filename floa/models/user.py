from floa.extensions import db
from floa.models.library import Library
from flask_login import UserMixin


class User(UserMixin):
    ''' User object

        id: private member for database record key
        uid: UUID for use in browser cookie and session to allow session
             invalidation
    '''
    def __init__(self, key, name, email, library, created_date, uid=None):
        self._key = key
        self.name = name
        self.email = email
        self.library = library
        self.created_date = created_date
        # flask_login UserMixin id attribute is our uid
        self.id = uid

    @staticmethod
    def init(record):
        user = User(
            key=record.get('key'),
            name=record.get('name'),
            email=record.get('email'),
            library=Library(library=record.get('library')),
            created_date=record.get('created_date'),
            uid=record.get('uid')
        )
        return user

    @staticmethod
    def get(user_id):
        ''' user_id == uid '''
        user = None
        record = db.query('uid', user_id)
        if record:
            user = User.init(record)
        return user

    @staticmethod
    def new(name, email):
        record = db.create(name, email)
        return User.init(record)

    @staticmethod
    def get_by_email(email):
        user = None
        record = db.query('email', email)
        if record:
            user = User.init(record)
        return user
