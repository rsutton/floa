import enum
import json


class Status(enum.Enum):
    MISSING = -1
    NOT_HAVE = 0
    HAVE = 1
    WISH = 2
    NEW  = 3


class Library(object):

    def __init__(self, library=None):
        self._library = library or [-1]

    @property
    def library(self):
        return self._library

    @library.setter
    def library(self, val):
        assert(isinstance(val, list))
        assert(val[0] == -1)
        self._library = val

    def set_status(self, id, status):
        if not isinstance(id, int):
            id = int(id)
        self.library[id] = status

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
        return self

    def import_json(self, fname):
        with open(fname, 'r') as f:
            self.library = json.load(f)

    def export_json(self, fname):
        with open(fname, 'w') as f:
            json.dump(self.library, f)

    def dump(self):
        print(str(self.library)[1:-1])
