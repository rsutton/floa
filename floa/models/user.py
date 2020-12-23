from floa.models.db import get_db


class User(object):
    def __init__(self, id, name, email, library=[-1]):
        self._id = id
        self.name = name
        self.email = email
        self._library = library

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
                    library=u.get('library')
                )
        return user

    # @staticmethod
    # def create(id, name, email, library=[-1])
    #     db = get_db()
    #     db
