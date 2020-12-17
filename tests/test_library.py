from flask import Flask
import json
import os
import os.path
import unittest

class TestLibrary(unittest.TestCase):

    def setUp(self) -> None:
        self.app = Flask(__name__)
        self.app.config.from_pyfile('config.py')
        self.app.config['TESTING'] = True

    def tearDown(self) -> None:
        return super().tearDown()

    def test_update_library(self):
        with self.app.app_context():
            import floa.routes as fr
            lib_filename = './tests/data/library_4_items.json'
            if os.path.isfile(lib_filename):
                os.remove(lib_filename)
            
            cat_filename = './tests/data/loa_catalog_4_items.data'
            catalog_4 = fr.load_catalog(filename=cat_filename)
            
            # create and save library
            fr.update_library(library=[], items=catalog_4, filename=lib_filename)
            # read library from file
            library = fr.load_library(filename=lib_filename)

            self.assertTrue(isinstance(library, list))
            self.assertEqual(len(library), len(catalog_4))
            
            