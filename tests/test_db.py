from flask import Flask, current_app as app, g
import floa.models.db as db
import pickle
from random import randrange
import unittest


class TestDatabase(unittest.TestCase):

    def _generate_database(self, count, start=0):
        result = []
        for i in range(start, count):
            lib_len = randrange(400)
            lib = self._generate_library(lib_len)
            result.append(
                {
                    'id': i,
                    'name': f'user-{i}',
                    'email': f'user-{i}@foo.com',
                    'library': lib
                })
        return result

    def _generate_library(self, count):
        result = [-1]
        for _ in range(1, count):
            result.append(randrange(-1, 3))
        return result

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_pyfile('config.py')
        self.filename = self.app.config['DATABASE']
        self.db = db.Database(filename=self.filename)

    def tearDown(self):
        pass

    def test_open(self):
        # manually create a database file
        num_records = 10
        records = self._generate_database(num_records)
        with open(self.filename, 'wb') as f:
            pickle.dump(records, f)

        # load the data
        with self.app.app_context():
            records = self.db.load()
        id = randrange(len(records))
        self.assertEqual(records[id].get('id'), id)
        self.assertEqual(len(records), num_records)

    def test_commit_db(self):
        # manually create database
        num_records = 2
        records = self._generate_database(num_records)
        with open(self.filename, 'wb') as f:
            pickle.dump(records, f)

        with self.app.app_context():
            # load the data
            records = self.db.load()
            # add another record
            records.append(self._generate_database(1, start=num_records))
            # commit it
            count = self.db.commit(records)
            self.assertEqual(count, num_records + 1)
            # reload and check
            records = self.db.load()
            self.assertEqual(len(records), count)
