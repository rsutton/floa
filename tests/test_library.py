import filecmp
from flask import Flask
from floa.models.library import Library, Status
import os.path
import random
import unittest
import json

class TestLibrary(unittest.TestCase):

    @staticmethod
    def _generate_catalog_list(count, start=1):
        result = []
        for i in range(start, start + count):
            result.append({'id': i, 'title': f'Title {i}'})
        return result
    
    @staticmethod
    def _generate_library_list(count, val=0, rand=False):
        result = [-1] 
        for i in range(1, count):
            if rand:
                val = random.randrange(-1,3)
            result.append(val)
        return result

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_pyfile('config.py')
        self.app.config['TESTING'] = True
        self.library = Library(ctx=self.app)

    def tearDown(self):
        return super().tearDown()

    def test_save_load(self):
        list10 = self._generate_library_list(10, 3)
        self.library.library = list10
        self.library.save().load()
        self.assertEqual(list10, self.library.library)

# this is a bad test
    def test_set_status(self):
        self.library.load()
        self.library.library = [-1,0,1,2,3]
        self.assertEqual(Status(self.library.library[1]), Status['NOT_HAVE'])
        self.assertEqual(Status(self.library.library[2]), Status['HAVE'])
        self.assertEqual(Status(self.library.library[3]), Status['WISH'])
        self.assertEqual(Status(self.library.library[4]), Status['NEW'])

    def test_add_book_status_value_is_new(self):
        list1 = self._generate_catalog_list(4)
        self.library.catalog = list1 
        # add some items
        self.library.update(self.library.catalog)
        # status of all is New
        for i in self.library.library:
            self.assertEqual(Status(self.library.library[i]), Status['NEW'])
        # and we have the whole list, +1
        self.assertEqual(len(self.library.library), 5)
        # add another item
        list2 = self._generate_catalog_list(5)
        # diff = self.library.compare(list1, list2)
        self.library.update(list2)
        self.assertEqual(len(self.library.library), 6)
        self.assertEqual(Status(self.library.library[4]), Status['NEW'])

    def test_add_with_insertion_of_missing_volume(self):
        list1 = self._generate_library_list(10, val=3)
        list1[8] = -1
        list1[9] = 2
        self.library.library = list1
        list2 = self._generate_catalog_list(4, start=8)
        self.library.update(list2)
        self.assertEqual(self.library.library[8], 3)
        self.assertEqual(self.library.library[9], 2)
        self.assertEqual(len(self.library.library), 12)

    def test_save_creates_folder(self):
        fname = './tests/tmp/file.tmp'
        self.library.filename=fname
        self.library.save()
        self.assertTrue(os.path.exists(fname))
        # cleanup
        os.remove(fname)
        os.rmdir(os.path.dirname(fname))
        self.assertFalse(os.path.exists(fname))

    def test_import_export_my_library(self):
        src='./tests/data/import.txt'
        dst='./tests/data/export.txt'
        list10 = self._generate_library_list(10, rand=True)
        with open(src, 'w') as f:
            json.dump(list10, f)
        self.library.import_json(fname=src)
        self.library.export_json(fname=dst)
        self.assertTrue(filecmp.cmp(src,dst))
        os.remove(src)
        os.remove(dst)