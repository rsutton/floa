from flask import Flask
import json
import unittest

class TestCatalog(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_pyfile('config.py')
        self.app.config['TESTING'] = True
        with self.app.app_context():
            from floa.models.catalog import Catalog
        self.catalog = Catalog(fname=self.app.config['CATALOG_FILENAME'])

    def tearDown(self):
        return super().tearDown()

    def test_catalog_is_valid_json(self):
        self.catalog.load()
        assert(isinstance(self.catalog.catalog, list))

    def test_catalog_no_diff(self):
        self.catalog.load()
        diff = self.catalog.compare(self.catalog.catalog, self.catalog.catalog)
        self.assertTrue(isinstance(diff, list))
        self.assertEqual(len(diff), 0)

    # def test_get_latest_catalog(self):
    #     ''' this is expensive and should be an integration test'''
    #     url=self.app.config['LOA_COLLECTION_URL']
    #     result = self.catalog.get_latest(url)
    #     assert(isinstance(result, list))
    #     id = result[0].get('id')
    #     self.assertTrue(id == 1)

    def test_catalog_with_one_diff(self):
        catold = self.catalog.load(fname='./tests/data/catalog-old.json').catalog
        catnew = self.catalog.load(fname='./tests/data/catalog-new.json').catalog
        diff = self.catalog.compare(catold, catnew)
        self.assertEqual(len(diff), 2)