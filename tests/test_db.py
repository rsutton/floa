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

    def test_commit(self):
        records = utils.generate_database(self.num_of_records)
        for r in records:
            key = self.db.commit(r)
        result = self.db.query(field='key', value=2)
        self.assertEqual(result.get('key'), 2)

    def test_commit_with_unset_key(self):
        records = utils.generate_database(1)
        for r in records:
            # -1 means key is not set
            r['key'] = -1
            result = self.db.commit(r)
            self.assertTrue(result != -1)
            # key should be set to next number, which should
            # be 1 since this is the first record
        result = self.db.query(field='key', value=1)
        self.assertEqual(result.get('key'), 1)

    def test_load(self):
        with self.app.app_context():
            records = self.db.load()
        key = len(records)
        # keys start at 1, so subtract 1 when using
        # 'key' as index  
        self.assertEqual(records[key-1].get('key'), key)

    def test_query_returns_results(self):
        result = self.db.query('key', self.num_of_records)
        self.assertIsNotNone(result)
        self.assertEqual(result.get('key'), self.num_of_records)

    def test_query_returns_none(self):
        result = self.db.query('key', self.num_of_records + 2)
        self.assertIsNone(result)
