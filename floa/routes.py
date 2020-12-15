
from flask import Blueprint, render_template, jsonify, request
from flask import current_app as app
import json
import os.path

bp = Blueprint(
    'home',
    'routes',
    url_prefix="/"
)

# globals
library_file = os.path.join(os.path.dirname(app.instance_path), app.config['LIBRARY_FILENAME'])
catalog_file = os.path.join(os.path.dirname(app.instance_path), app.config['CATALOG_FILENAME'])

@bp.route("/")
def home():
    return render_template('home.html', list=library)

def find_by_id(id):
    if isinstance(id, str):
        id = int(id)

    for item in library:
        if item['id'] == id:
            return item
    return {}

@bp.route("/_update", methods=["POST"])
def update_book_status():
    id = request.json['id']
    status = request.json['status']
    if isinstance(status, str):
        status = int(status)

    item = find_by_id(id)
    if len(item) > 0:
        item['status'] = status
        save_library()
        return id
    return {}

@bp.route("/_check")
def check_for_updates():
    load_catalog()

    loa_latest = get_latest_loa_catalog()
    loa_diff = get_list_difference(loa_latest, catalog)

    if len(loa_diff) > 0:
        # TODO
        # should return list of updates for user to accept/decline
        # instead of automerging

        # loa_latest is authoritative so overwrite the catalog
        overwrite_catalog_with(loa_latest)
        # add new items to library
        update_library_with(loa_diff)
        return render_template('catalog.html', list=loa_diff)

    return render_template('catalog.html', list=empty_list(0, "No Updates Found"))

def get_latest_loa_catalog():
    ''' webscrape to create a list of LoA titles '''
    import requests
    from bs4 import BeautifulSoup  
    url = app.config['LOA_COLLECTION_URL']
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    books = soup.find_all('li', class_='content-listing--book')
    result = []

    for book in books:
        id = int(book.find('i', class_='book-listing__number').text)
        title = book.find('b', class_='content-listing__title').text
        link = app.config['LOA_BASE_URL'] + book.find('a')['href']
        book = {"id": id, "title": title, "link": link}
        result.append(book)
    return result

# List Helpers
def get_list_difference(list1, list2):
    diff = [i for i in list1 + list2 if i not in list1 or i not in list2]
    return diff

def empty_list(id=0, title='NA', link=''):
    return [{'id': id, 'title': title, 'link': link, 'status': 0}]

def write_list_to_file(lst, fname):
    json.dump(lst, open(fname, 'w'))

def read_list_from_file(fname):
    return json.load(open(fname, 'r'))

# Library helpers
def save_library():
    write_list_to_file(library, library_file)
    load_library()

def load_library():
    global library 
    try:
        library = read_list_from_file(library_file)
    except:
        library = create_library()

def create_library():
    global library
    library = []
    load_catalog()
    update_library_with(catalog)
    return library

def update_library_with(items):
    for item in items:
        book = find_by_id(item['id'])
        if len(book) > 0:
            for key in item.keys():
                book[key] = item[key]
        else:
            item['status'] = 0
            library.append(item)
    save_library()


# Catalog helpers
def save_catalog():
    write_list_to_file(catalog, catalog_file)
    load_catalog()

def load_catalog():
    global catalog
    try:
        catalog = read_list_from_file(catalog_file)
    except:
        catalog = get_latest_loa_catalog()
        save_catalog()

def overwrite_catalog_with(lst):
    write_list_to_file(lst, catalog_file)
    load_catalog()
