from flask import Flask

import unittest

class TestCatalog(unittest.TestCase):

    def setUp(self) -> None:
        self.app = Flask(__name__)
        self.app.config.from_pyfile('config.py')
        self.app.config['TESTING'] = True

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_list_diff(self):
        with self.app.app_context():
            import floa.routes as fr
            catalog_4 = fr.load_catalog(filename='./tests/data/loa_catalog_4_items.data')
            catalog_8 = fr.load_catalog(filename='./tests/data/loa_catalog_8_items.data')
            diff = fr.get_list_diff(catalog_4, catalog_8)
            self.assertEqual(len(diff), 4)
            diff = fr.get_list_diff(catalog_4, catalog_4)
            self.assertEqual(len(diff), 0)


