from flask import current_app as app, g
import os
import os.path
import pickle

empty_db = [{'library': []}]


def get_db():
    database = app.config['DATABASE']
    if 'db' not in g:
        try:
            with open(database, 'rb+') as f:
                g.db = pickle.load(f)
        except EOFError as e:
            g.db = empty_db
    return g.db


def commit(data):
    database = app.config['DATABASE']
    with open(database, 'wb') as f:
        pickle.dump(data, f)
    return len(data)


def close_db():
    g.pop('db', None)
