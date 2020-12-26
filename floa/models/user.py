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
        'key': -1,
        'id': None,
        'name': None,
        'email': None,
        'library': None,
        'created_date': dt.now(),
        }

    def __init__(self, name, email, **kwargs):
        self.name = name
        self.email = email
        self._key = kwargs.get('key') or -1
        self.id = kwargs.get('id') or None
        self.library = kwargs.get('library') or Library()
        self.created_date = kwargs.get('created_data') or dt.now()

    def __repr__(self):
        return {
                'key': self._key,
                'id': self.id,
                'name': self.name,
                'email': self.email,
                'library': self.library,
                'created_date': self.created_date
            }

    @staticmethod
    def user_from_record(record):
        user = User(
            key=record.get('key'),
            id=record.get('id'),
            name=record.get('name'),
            email=record.get('email'),
            library=Library(library=record.get('library')),
            created_date=record.get('created_date')
        )
        return user

    @staticmethod
    def get(user_id):
        user = None
        record = db.query('id', user_id)
        if record:
            user = User.user_from_record(record)
        return user

    def add(self):
        self._key = db.commit(self.__repr__())

    @staticmethod
    def get_by_email(email):
        user = None
        record = db.query('email', email)
        if record:
            user = User.user_from_record(record)
        return user
