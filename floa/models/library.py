import datetime as dt

import enum
import os.path
import pickle

class Status(enum.Enum):
    MISSING = -1
    NOT_HAVE = 0
    HAVE = 1
    WISH = 2
    NEW  = 3

class Library(object):

    def __init__(self, *args, **kwargs):
        self._library = [-1]
        self._filename = kwargs.get('fname') or None

        if 'ctx' in kwargs:
            ctx = kwargs.get('ctx')
            self._filename = os.path.join(
                os.path.dirname(ctx.instance_path), 
                ctx.config['LIBRARY_FILENAME'])

    @property
    def library(self):
        return self._library

    @library.setter
    def library(self, val):
        assert(isinstance(val, list))
        self._library = val

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, val):
        assert(isinstance(val, str))
        self._filename = val
    
    def load(self, fname=None):
        if fname is None:
            fname = self.filename
        if os.path.exists(fname):
            with open(fname, 'rb') as f:
                p = pickle.load(f)
                self.__dict__.clear()
                self.__dict__.update(p.__dict__) 
        return self
         
    def save(self, fname=None):
        if fname is None:
            fname = self.filename
        if not os.path.exists(os.path.dirname(fname)):
            os.makedirs(os.path.dirname(fname))
        with open(fname, 'wb') as f:
            pickle.dump(self, f)
        return self

    def set_status(self, id, status):
        if not isinstance(id, int):
            id = int(id)
        self.library[id] = status
        self.save()

    def update(self, items):
        for item in items:
            nl = len(self.library)
            id = item.get('id')
            while (id > nl):
                self.library.append(-1)
                nl = len(self.library)
            if (id < nl):
                if self.library[id] == Status.MISSING.value:
                    self.library[id] = Status.NEW.value
            else:
                self.library.append(Status.NEW.value)
        self.save().load()

 