from floa.extensions import db
from floa.models.library import Library


class User(object):
    def __init__(self, id, name, email, library, created_date):
        self.id = id
        self.name = name
        self.email = email
        self.library = library
        self.created_date = created_date

    @staticmethod
    def get(user_id):
        record = db.get_user_by_id(user_id)
        if record:
            user = User(
                id=record.get('id'),
                name=record.get('name'),
                email=record.get('email'),
                library=Library(library=record.get('library')),
                created_date=record.get('created_date')
            )
        return None

    @staticmethod
    def create(id, name, email, library, created_date):
        pass
