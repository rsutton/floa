from filelock import FileLock
from flask import g
import os
import pickle


class Database(object):

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
            if record.get('key') == -1:
                key = len(data)
                record['key'] = key
            data.append(record)
            # return to beginning of file since
            # we are overwriting all of the data
            f.seek(0)
            pickle.dump(data, f)
            f.close()
        self.lock.release()
        return record.get('key')

    def query(self, field, value):
        data = self.load()
        for u in data:
            if u.get(field) == value:
                return u

    @staticmethod
    def get_pickle_data(filehandle):
        try:
            data = pickle.load(filehandle)
        except EOFError:
            data = []
        except OSError as e:
            print(f'Error during data load: {e}')
            raise
        return data
