from flask import Flask
import json
import os.path
import unittest

class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_pyfile('config.py')
        self.app.config['TESTING'] = True
        with self.app.app_context():
            from floa.models.library import Library
        self.library = Library(self.app)

    def tearDown(self):
        return super().tearDown()
            
    def test_library_from_file_is_valid_json(self):
        self.library.load()
        lib = self.library.library
        assert(isinstance(lib, list))
        json.dumps(lib)

    def test_find_by_id_found_returns_valid(self):
        self.library.load()
        result = self.library.find_by_id(1)
        self.assertEqual(1, result.get('id'))

    def test_find_by_id_not_found_returns_empty(self):
        self.library.load()
        id = self.library.library[-1].get('id') + 1
        result = self.library.find_by_id(id)
        self.assertEqual(len(result), 0)

    def test_set_book_status_success(self):
        self.library.load()
        status = self.library.book_status(1)
        assert(isinstance(status, int))
        self.assertTrue(status <= 4)

    def test_set_book_status_fail(self):
        self.library.load()
        id = self.library.library[-1].get('id') + 1

        status = self.library.book_status(id)
        assert(isinstance(status, int))
        self.assertTrue(status == 0)        