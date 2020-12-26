from datetime import datetime as dt
from random import randrange
from uuid import uuid4


def generate_database(count, start=0):
    result = []
    for i in range(start, count):
        lib_len = randrange(10)
        lib = generate_library(lib_len)
        result.append(
            {
                'key': i,
                'name': f'user-{i}',
                'email': f'user-{i}@foo.com',
                'library': lib,
                'created_date': dt.now(),
                'uid': str(uuid4())
            })
    return result


def generate_library(count):
    result = [-1]
    for _ in range(1, count):
        result.append(randrange(-1, 3))
    return result
