from flask import Flask
from floa.models.catalog import Catalog
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
        self.catalog = Catalog(self.app).save()

    def tearDown(self):
        return super().tearDown()

    def test_catalog_compare_no_diff(self):
        list1 = self.generate_list(3)
        diff = self.catalog.compare(list1, list1)
        self.assertTrue(isinstance(diff, list))
        self.assertEqual(len(diff), 0)

    # def test_get_latest_catalog(self):
    #     ''' this is expensive and should be an integration test'''
    #     url=self.app.config['LOA_COLLECTION_URL']
    #     result = self.catalog.get_latest(url)
    #     assert(isinstance(result, list))
    #     id = result[0].get('id')
    #     self.assertTrue(id == 1)

    def test_catalog_compare_with_one_diff(self):
        diff = self.catalog.compare(self.generate_list(2), self.generate_list(3))
        self.assertEqual(len(diff), 1)