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
        result = self.db.query(field='name', value=f'user-{self.num_of_records - 1}')
        self.assertEqual(result.get('name'), f'user-{self.num_of_records - 1}')

    def test_commit_new_record(self):
        records = utils.generate_database(1, start=self.num_of_records)
        self.num_of_records += 1
        for r in records:
            result = self.db.commit(r)
        # result is index of record. index starts at 0
        # so len -1 is correct value
        last_idx = len(self.db._data) - 1
        self.assertTrue(result == last_idx)
        username = f'user-{last_idx}'
        result = self.db.query(field='name', value=username)
        self.assertEqual(result.get('name'), username)

    def test_commit_update_record(self):
        username = f'user-{self.num_of_records - 2}'
        record = self.db.query(field='name', value=username)
        record['name'] = 'update'
        idx = self.db.commit(record)
        self.assertTrue(self.db._data[idx]['name'] == 'update')

    def test_query_returns_results(self):
        username = f'user-{self.num_of_records - 1}'
        result = self.db.query('name', username)
        self.assertIsNotNone(result)

    def test_query_returns_none(self):
        result = self.db.query('foo', 'bar')
        self.assertIsNone(result)

    def test_rebuild_index(self):
        index = self.db.rebuild_index()
        result = self.db.query('name', f'user-{self.num_of_records - 1}')
        self.assertEqual(index[result['id']], self.db._data.index(result))
