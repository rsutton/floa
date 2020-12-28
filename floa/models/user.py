from datetime import datetime as dt
from floa.extensions import db
from floa.models.library import Library
from flask_login import UserMixin


class User(UserMixin):
    ''' User object

        key: private member for database record key
        id: UUID for use in browser cookie and session to allow session
             invalidation
    '''

    fields = {
        'id': None,
        'name': None,
        'email': None,
        'library': None,
        'created_date': dt.now(),
        'deleted_date': None,
        }

    def __init__(self, name, email, **kwargs):
        self.name = name
        self.email = email
        self.id = kwargs.get('id') or None
        self.library = kwargs.get('library') or Library()
        self.created_date = kwargs.get('created_data') or dt.now()
        self.deleted_date = None

    def __repr__(self):
        return {
                'id': self.id,
                'name': self.name,
                'email': self.email,
                'library': self.library.library,
                'created_date': self.created_date,
                'deleted_date': self.deleted_date,
            }

    def save(self):
        idx = db.commit(self.__repr__())
        return idx

    @staticmethod
    def user_from_record(record):
        user = User(
            id=record.get('id'),
            name=record.get('name'),
            email=record.get('email'),
            library=Library(library=record.get('library')),
            created_date=record.get('created_date'),
            deleted_date=record.get('deleted_date')
        )
        return user

    @staticmethod
    def get(user_id):
        user = None
        record = db.query('id', user_id)
        if record:
            user = User.user_from_record(record)
        return user

    @staticmethod
    def get_by_email(email):
        user = None
        record = db.query('email', email)
        if record:
            user = User.user_from_record(record)
        return user
