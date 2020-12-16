from bs4 import BeautifulSoup 
from flask import Blueprint, render_template, jsonify, request
from flask import current_app as app
import json
import os.path
import pickle
import requests

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
    library = load_library()
    return render_template('home.html', list=library)

@bp.route("/_update/item", methods=["POST"])
def update_book_status():
    id = request.json['id']
    status = request.json['status']
    if isinstance(status, str):
        status = int(status)
    library = load_library()
    item = find_by_id(library, id)
    if len(item) > 0:
        item['status'] = status
        save_library(library)
        return id
    return {}

@bp.route("/_update/catalog")
def update_catalog():
    library = load_library()
    catalog = load_catalog()
    latest = get_latest_catalog()
    diff = get_list_diff(latest, catalog)
    if len(diff) > 0:
        # latest is authoritative so overwrite the catalog
        save_catalog(latest)
        # add new items to library
        update_library(library, diff)
    return jsonify(diff)

def get_latest_catalog():
    ''' webscrape to create a list of LoA titles ''' 
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
def get_list_diff(list1, list2):
    diff = [i for i in list1 + list2 if i not in list1 or i not in list2]
    return diff

def write_list_to_file(lst, fname):
    json.dump(lst, open(fname, 'w'))

def read_list_from_file(fname):
    return json.load(open(fname, 'r'))

# Library helpers
def find_by_id(library, id):
    if isinstance(id, str):
        id = int(id)

    for item in library:
        if item['id'] == id:
            return item
    return {}

def save_library(library):
    write_list_to_file(library, library_file)

def load_library():
    try:
        library = read_list_from_file(library_file)
    except:
        library = create_library()
    return library

def create_library():
    library = []
    catalog = get_latest_catalog()
    save_catalog(catalog)
    update_library(library, catalog)
    return library

def update_library(library, items):
    for item in items:
        book = find_by_id(library, item['id'])
        if len(book) > 0:
            for key in item.keys():
                book[key] = item[key]
        else:
            item['status'] = 3
            library.append(item)
    save_library(library)


# Catalog helpers
def save_catalog(obj):
    with open(catalog_file, 'wb') as f:
        pickle.dump(obj, f)

def load_catalog():
    try:
        with open(catalog_file, 'rb') as f:
            catalog = pickle.load(f)
    except:
        catalog = []
    return catalog
