import json
import os.path

class Library(object):
    def __init__(self, **kwargs):
        self._library = None
        self._filename = kwargs.get('fname') or None
        self._app = kwargs.get('app') or None

        if self._app is not None:
            self._filename = os.path.join(
                    os.path.dirname(self._app.instance_path), 
                    self._app.config['LIBRARY_FILENAME'])

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

    def from_list(self, obj):
        pass

    def load(self, fname=None):
        if fname is None:
            fname = self._filename
        with open(fname, 'r') as f:
            self._library = json.load(f)
        return len(self._library)

    def save(self, fname=None):
        if fname is None:
            fname = self._filename        
        with open(fname, 'w') as f:
            json.dump(self._library, f)
        return len(self._library)

    def book_status(self, id):
        item = self.find_by_id(id)
        if len(item) > 0:
            return id
        return 0

    def set_book_status(self, id, status):
        item = self.find_by_id(id)
        if len(item) > 0:
            item['status'] = status
            self.save()
            return id
        return 0

    def find_by_id(self, id):
        if isinstance(id, str):
            id = int(id)

        for item in self.library:
            if item['id'] == id:
                return item
        return {}

    def add(self, items):   
        for item in items:
            book = self.find_by_id(item.get('id'))
            if len(book) > 0:
                for key in item.keys():
                    book[key] = item[key]
            else:
                item['status'] = 3
                self.library.append(item)
        self.save()
