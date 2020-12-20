from flask import Flask
from floa.models import library
from floa.models.library import Library, Status
import unittest
import random

class TestCatalog(unittest.TestCase):

    @staticmethod
    def generate_catalog_list(count, start=1, rand=False):
        result = []
        for i in range(start, start + count):
            id = i
            if rand:
                id = random.randrange(400)
            result.append({'id': id, 'title': f'Title {i}'})
        return result
    
    @staticmethod
    def generate_library_list(count, val=None, rand=False):
        result = [-1] 
        if val is None:
            rand = True
        for i in range(1, count):
            if rand:
                val = random.randint(0, 3)
            result.append(val)
        return result

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_pyfile('config.py')
        self.app.config['TESTING'] = True
        self.library = Library(self.app).save()

    def tearDown(self):
        return super().tearDown()

    def test_catalog_compare_no_diff(self):
        list1 = self.generate_catalog_list(3)
        diff = self.library.compare(list1, list1)
        self.assertTrue(isinstance(diff, list))
        self.assertEqual(len(diff), 0)

    # def test_get_latest_catalog(self):
    #     ''' this is expensive and should be an integration test'''
    #     url=self.app.config['LOA_COLLECTION_URL']
    #     result = self.library.get_latest(url)
    #     assert(isinstance(result, list))
    #     id = result[0].get('id')
    #     self.assertTrue(id == 1)

    def test_catalog_compare_with_one_diff(self):
        diff = self.library.compare(self.generate_catalog_list(2), self.generate_catalog_list(3))
        self.assertEqual(len(diff), 1)

    def test_find_by_id_found_returns_valid(self):
        self.library.load()
        self.library.catalog = self.generate_catalog_list(4)
        result = self.library.find_by_id(1)
        assert(isinstance(result, dict))
        self.assertEqual(1, result.get('id'))

    def test_find_by_id_not_found_returns_empty(self):
        self.library.load()
        self.library.catalog = self.generate_catalog_list(4)
        id = self.library.catalog[-1].get('id') + 1
        result = self.library.find_by_id(id)
        assert(isinstance(result, dict))
        self.assertEqual(len(result), 0)

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

    def test_sort_catalog(self):
        list1 = self.generate_catalog_list(100, rand=True)
        sorted_list = self.library.sort(lst=list1)
        for i in range(len(sorted_list) - 1):
            self.assertTrue(sorted_list[i]['id'] <= sorted_list[i+1]['id'])

    def test_add_with_non_consecutive_id(self):
        list1 = self.generate_library_list(10, val=3)
        list1[8] = -1
        list1[9] = 2
        self.library.library = list1
        list2 = self.generate_catalog_list(4, start=8)
        self.library.add(list2)
        self.assertEqual(self.library.library[8], 3)
        self.assertEqual(self.library.library[9], 2)
        self.assertEqual(len(self.library.library), 12)