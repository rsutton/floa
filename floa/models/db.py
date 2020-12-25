from datetime import datetime as dt
from filelock import FileLock
from flask import g
import os
import pickle
from uuid import uuid4

class Database(object):

    empty_database = [{
        'key': 0,
        'name': None,
        'email': None,
        'library': None,
        'created_date': None,
        'uid': None
        }]

    fields = [
        'key',
        'name',
        'email',
        'library',
        'created_date',
        'uid'
        ]

    def __init__(self, filename=None, app=None):
        self.filename = filename
        self._db_len = None
        self.app = app

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
                self._db_len = len(data)
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

    def query(self, field, value):
        data = self.load()
        for u in data:
            if u.get(field) == value:
                return u

    def create(self, name, email):
        lock = FileLock(".".join(self.filename, 'lock'))
        with lock:
            data = self.load()
            record = {
                'key': len(data),
                'name': name,
                'email': email,
                'library': [-1],
                'created_date': dt.now(),
                'uid': str(uuid4())
                }
            data.append(record)
            self.commit(data)
        return record
