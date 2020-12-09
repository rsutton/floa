
from flask import Blueprint, render_template, jsonify
from flask import current_app as app
import json

bp = Blueprint(
    'home',
    'routes',
    url_prefix="/"
)

@bp.route("/")
def home():
    return render_template('home.html', library=library)

@bp.route("/<id>")
def find_by_id(id):
    for i in library:
        if i['id'] == int(id):
            return render_template('list.html', list=[i])
    return render_template('list.html', list=[{'id': id, 'title': "Item does not exist"}])

@bp.route("/have/<id>")
def have(id):
    item = find_by_id(id)
    item['have'] = 1
    item['want'] = 0
    save_library()
    return item

@bp.route("/want/<id>")
def want(id):
    item = find_by_id(id)
    item['have'] = 0
    item['want'] = 1
    save_library()
    return item

@bp.route("/title/<query>")
def find_title(query):
    results = []
    q = query.lower()
    for i in library:
        if q in i['title'].lower():
            results.append(i)
    return render_template('list.html', list=results)

@bp.route("/list")
def list():
    return render_template('list.html', list=library)

def get_latest_loa_catalog():
    ''' webscrape to create a list of LoA titles '''
    import requests
    from bs4 import BeautifulSoup  
    url = 'https://loa.org/books/loa_collection'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    books = soup.find_all('li', class_='content-listing--book')
    result = []

    for book in books:
        id = int(book.find('i', class_='book-listing__number').text)
        title = book.find('b', class_='content-listing__title').text
        book = {"id": id, "title": title}
        result.append(book)
    return result

def get_list_difference(list1, list2):
    diff = [i for i in list1 + list2 if i not in list1 or i not in list2]
    return diff

@bp.route("/update")
def check_for_update():
    load_catalog()

    loa_latest = get_latest_loa_catalog()
    loa_diff = get_list_difference(loa_latest, catalog)

    message = "No updates, {} records".format(len(loa_latest))
    if len(loa_diff) > 0:
        message = "Found {} new records {}".format(len(loa_diff), loa_diff)
        # loa_latest is authoritative so overwrite 
        overwrite_catalog_with(loa_latest)
        for i in loa_diff:
            add_to_library(i['id'], i['title'])

    return message


def write_list_to_file(lst, fname):
    json.dump(lst, open(fname, 'w+'))

def read_list_from_file(fname):
    return json.load(open(fname, 'r'))

def save_library():
    write_list_to_file(library, './floa/library.json')
    load_library()

def load_library():
    global library 
    library = read_list_from_file('./floa/library.json')

def add_to_library(id, title):
    library.append({'id': id, 'title': title, 'have': 0, 'want': 0})
    save_library()

def save_catalog():
    write_list_to_file(catalog, './floa/loa_catalog.json')
    load_catalog()

def load_catalog():
    global catalog
    catalog = read_list_from_file('./floa/loa_catalog.json')

def overwrite_catalog_with(lst):
    write_list_to_file(lst, './floa/loa_catalog.json')
    load_catalog()

load_library()