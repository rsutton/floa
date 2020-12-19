from flask import Flask
from floa.models.library import Library
import unittest

class TestCatalog(unittest.TestCase):

    @staticmethod
    def generate_list(count):
        result = []
        for i in range(count):
            result.append({'id': i, 'title': f'Title {i}'})

        return result

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_pyfile('config.py')
        self.app.config['TESTING'] = True
        self.library = Library(self.app).save()

    def tearDown(self):
        return super().tearDown()

    def test_catalog_compare_no_diff(self):
        list1 = self.generate_list(3)
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
        diff = self.library.compare(self.generate_list(2), self.generate_list(3))
        self.assertEqual(len(diff), 1)

    def test_find_by_id_found_returns_valid(self):
        self.library.load()
        self.library.catalog = self.generate_list(4)
        result = self.library.find_by_id(1)
        self.assertEqual(1, result.get('id'))

    def test_find_by_id_not_found_returns_empty(self):
        self.library.load()
        self.library.catalog = self.generate_list(4)
        id = self.library.catalog[-1].get('id') + 1
        result = self.library.find_by_id(id)
        self.assertEqual(len(result), 0)

    def test_set_book_status(self):
        self.library.load()
        list1 = self.generate_list(4)
        self.library.catalog = list1 
        self.library.add(self.library.catalog)
        self.assertEqual(self.library.library[0], 3)
        self.assertEqual(len(self.library.library), 4)
        list2 = self.generate_list(5)
        diff = self.library.compare(list1, list2)
        self.library.add(diff)
        self.assertEqual(len(self.library.library), 5)
        self.assertEqual(self.library.library[4], 3)
        print(self.library.library)

# need to test gaps in id numbers
