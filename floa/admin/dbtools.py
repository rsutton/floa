from datetime import datetime as dt
import pickle
from uuid import uuid4
import io
import binascii

filename = '../../instance/myloa.data'

with open(filename, 'rb') as f:
    data = pickle.load(f)
    # print(data)
    record = [{
        'id': str(uuid4()),
        'name': data[0].get('name'),
        'email': data[0].get('email'),
        'library': data[0].get('library'),
        'created_date': data[0].get('created_date'),
        'deleted_date': data[0].get('deleted_date'),
        }]
    print(record)


with open(filename, 'wb') as f:
    pickle.dump(record, f)



# def unpickle_iter(file):
#     try:
#         while True:
#             yield pickle.load(file)
#     except EOFError:
#         pass


# with open('./instance/my-database.data', 'rb') as f:
#     for item in unpickle_iter(f):
#         print(item)