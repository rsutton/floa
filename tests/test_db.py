from flask import Flask
import floa.models.db as db
import os.path
import os
import unittest
from . import utils


class TestDatabase(unittest.TestCase):

    num_of_records = 4

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config.from_pyfile('config.py')
        cls.db = db.Database(app=cls.app)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.db.filename)
        os.remove(".".join([cls.db.filename, 'lock']))

    def test_init_db(self):
        self.assertTrue(os.path.exists(self.db.filename))

    def test_create(self):
        self.db.create(name="test_create", email="foo")
        result = self.db.query(field='name', value='test_create')
        key1 = result.get('key')
        self.assertIsNotNone(result)
        result = self.db.query(field='email', value='foo')
        key2 = result.get('key')
        self.assertIsNotNone(result)        
        self.assertEqual(key1, key2)

    def test_commit(self):
        records = utils.generate_database(self.num_of_records)
        for r in records:
            self.db.commit(r)
        result = self.db.query(field='key', value=2)
        self.assertEqual(result.get('key'), 2)

    def test_load(self):
        with self.app.app_context():
            records = self.db.load()
        key = len(records)-1
        self.assertEqual(records[key].get('key'), key)

    def test_query_returns_results(self):
        result = self.db.query('key', self.num_of_records - 1)
        self.assertIsNotNone(result)
        self.assertEqual(result.get('key'), self.num_of_records - 1)

    def test_query_returns_none(self):
        result = self.db.query('key', self.num_of_records + 1)
        self.assertIsNone(result)

    def test_query_with_invalid_field_raises_value_error(self):
        self.assertRaises(ValueError, self.db.query, 'foo', 'bar')
