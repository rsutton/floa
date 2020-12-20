from flask import Flask
from floa.models.library import Library, Status
import os.path
import unittest

class TestLibrary(unittest.TestCase):

    @staticmethod
    def generate_catalog_list(count, start=1):
        result = []
        for i in range(start, start + count):
            result.append({'id': i, 'title': f'Title {i}'})
        return result
    
    @staticmethod
    def generate_library_list(count, val):
        result = [-1] 
        for i in range(1, count):
            result.append(val)
        return result

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_pyfile('config.py')
        self.app.config['TESTING'] = True
        self.library = Library(ctx=self.app).save()

    def tearDown(self):
        return super().tearDown()

    def test_set_status(self):
        self.library.load()
        self.library.library = [-1,0,1,2,3]
        self.assertEqual(Status(self.library.library[1]), Status['NOT_HAVE'])
        self.assertEqual(Status(self.library.library[2]), Status['HAVE'])
        self.assertEqual(Status(self.library.library[3]), Status['WISH'])
        self.assertEqual(Status(self.library.library[4]), Status['NEW'])

    def test_add_book_status_value_is_new(self):
        self.library.load()
        list1 = self.generate_catalog_list(4)
        self.library.catalog = list1 
        # add some items
        self.library.add(self.library.catalog)
        # status of all is New
        for i in self.library.library:
            self.assertEqual(Status(self.library.library[i]), Status['NEW'])
        # and we have the whole list, +1
        self.assertEqual(len(self.library.library), 5)
        # add another item
        list2 = self.generate_catalog_list(5)
        diff = self.library.compare(list1, list2)
        self.library.add(diff)
        self.assertEqual(len(self.library.library), 6)
        self.assertEqual(Status(self.library.library[4]), Status['NEW'])

    def test_add_with_insertion_of_missing_volume(self):
        list1 = self.generate_library_list(10, val=3)
        list1[8] = -1
        list1[9] = 2
        self.library.library = list1
        list2 = self.generate_catalog_list(4, start=8)
        self.library.add(list2)
        self.assertEqual(self.library.library[8], 3)
        self.assertEqual(self.library.library[9], 2)
        self.assertEqual(len(self.library.library), 12)

    def test_catalog_compare_no_diff(self):
        list1 = self.generate_catalog_list(3)
        diff = self.library.compare(list1, list1)
        self.assertTrue(isinstance(diff, list))
        self.assertEqual(len(diff), 0)
        
    def test_catalog_compare_with_one_diff(self):
        list1 = self.generate_catalog_list(2)
        list2 = self.generate_catalog_list(3)
        diff = self.library.compare(list1, list2)
        self.assertEqual(len(diff), 1)

    def test_save_creates_folder(self):
        fname = './tests/tmp/file.tmp'
        self.library.filename=fname
        self.library.save()
        self.assertTrue(os.path.exists(fname))
        # cleanup
        os.remove(fname)
        os.rmdir(os.path.dirname(fname))
        self.assertFalse(os.path.exists(fname))
