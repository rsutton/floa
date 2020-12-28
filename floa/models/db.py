from filelock import FileLock
from flask import g
import os
import pickle


class Database(object):

    def __init__(self, filename=None, app=None):
        self.filename = filename
        self._data = []
        self._index = None
        self._lock = None
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
        self.load()

    @property
    def lock(self):
        if self._lock is None:
            lockfile = ".".join([self.filename, "lock"])
            timeout = -1
            self._lock = FileLock(lockfile, timeout)
        return self._lock

    def load(self):
        with self.lock.acquire():
            with open(self.filename, 'rb') as f:
                self._data = Database.get_pickle_data(f)
        self.lock.release()
        self.rebuild_index()

    def rebuild_index(self):
        self._index = {}
        for r in self._data:
            self._index[r['id']] = self._data.index(r)
            self._index[r['email']] = self._data.index(r)
        return self._index

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

    def commit(self, record):
        with self.lock.acquire():
            idx = None
            if record.get('id') not in self._index:
                # add new record
                # next index
                idx = len(self._data)
                self._data.append(record)
                self.rebuild_index()
            else:
                # update existing item
                idx = self._index[record.get('id')]
                item = self._data[idx]
                for k in record.keys():
                    item[k] = record[k]

                with open(self.filename, 'wb') as f:
                    pickle.dump(self._data, f)
        self.lock.release()
        return idx

    def query(self, field, value):
        for u in self._data:
            if u.get(field) == value:
                return u
