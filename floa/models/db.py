from flask import current_app as app, g
import pickle

empty_database = [{'id': 0, 'name': None, 'email': None, 'library': None}]

def get_db():
    database = app.config['DATABASE']
    if 'db' not in g:
        try:
            with open(database, 'rb+') as f:
                g.db = pickle.load(f)
        except:
            commit(empty_database)
            g.db = empty_database
    return g.db


def commit(data):
    database = app.config['DATABASE']
    with open(database, 'wb') as f:
        pickle.dump(data, f)
    return len(data)


def close_db():
    g.pop('db', None)
