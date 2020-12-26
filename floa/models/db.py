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
        self._lock = None
        self._db_len = None
        self.app = app

        if app is not None:
            self.init_db(app)

    def init_db(self, app):
        if not self.filename:
            self.filename = os.path.join(
                app.instance_path,
                app.config['DATABASE'])
        if not os.path.exists(self.filename):
            with open(self.filename, 'a'):
                try:
                    os.utime(self.filename, None)
                except OSError:
                    pass

    @property
    def lock(self):
        if self._lock is None:
            lockfile = ".".join([self.filename, "lock"])
            timeout = -1
            self._lock = FileLock(lockfile, timeout)
        return self._lock

    def get_db(self):
        if 'db' not in g:
            g.db = self
        return g.db

    def load(self):
        with self.lock.acquire():
            with open(self.filename, 'rb') as f:
                data = Database.get_pickle_data(f)
        self.lock.release()
        return data

    @staticmethod
    def close_db():
        g.pop('db', None)

    def commit(self, record):
        data = None
        with self.lock.acquire():
            f = open(self.filename, 'r+b')
            data = Database.get_pickle_data(f)
            data.append(record)
            # return to beginning of file since
            # we are overwriting all of the data
            f.seek(0)
            pickle.dump(data, f)
            f.close()
        self.lock.release()
        return len(data)

    def query(self, field, value):
        if field not in self.fields:
            raise ValueError(f'Invalid field: {field}')
        data = self.load()
        for u in data:
            if u.get(field) == value:
                return u

    def create(self, name, email):
        with self.lock.acquire():
            f = open(self.filename, 'r+b')
            data = Database.get_pickle_data(f)
            record = {
                'key': len(data),
                'name': name,
                'email': email,
                'library': [-1],
                'created_date': dt.now(),
                'uid': str(uuid4())
                }
            data.append(record)
            f.seek(0)
            pickle.dump(data, f)
            f.close()
        self.lock.release()
        return record

    @staticmethod
    def get_pickle_data(filehandle):
        try:
            data = pickle.load(filehandle)
        except EOFError:
            data = []
        return data
