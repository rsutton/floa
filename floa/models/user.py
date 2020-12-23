from floa.models.db import get_db
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
        user = None
        db = get_db()
        for u in db:
            if u.get('id') == user_id:
                user = User(
                    id=u.get('id'),
                    name=u.get('name'),
                    email=u.get('email'),
                    library=Library(library=u.get('library')),
                    created_date=u.get('created_date')
                )
        return user

    @staticmethod
    def create(id, name, email, library, created_date):
        pass
