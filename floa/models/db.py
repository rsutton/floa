from flask import current_app, g
import os
import pickle


class Database(object):

    empty_database = [{
        'id': 0,
        'name': None,
        'email': None,
        'library': None,
        'created_date': None
        }]

    fields = [
        'id',
        'name',
        'email',
        'library',
        'created_date'
        ]

    def __init__(self, filename=None, app=None):
        self.filename = filename
        self.app = app
        self._instance = None
        if app is not None:
            self.init_db(app)

    def init_db(self, app):
        self.filename = os.path.join(app.instance_path, app.config['DATABASE'])
        print(f"Initializing database...{self.filename}")
        if not os.path.exists(self.filename):
            with open(self.filename, 'a'):
                try:
                    os.utime(self.filename, None)
                except OSError:
                    pass

    def get_db(self):
        if 'db' not in g:
            g.db = self
        return g.db

    def load(self):
        with open(self.filename, 'rb+') as f:
            try:
                data = pickle.load(f)
            except EOFError:
                print("Empty database")
                data = self.empty_database
        return data

    def commit(self, data):
        with open(self.filename, 'wb') as f:
            pickle.dump(data, f)
        return len(data)

    @staticmethod
    def close_db():
        g.pop('db', None)

    def get_user_by_id(self, id):
        data = self.load()
        assert(isinstance(id, int))
        for u in data:
            if u.get('id') == id:
                return u
