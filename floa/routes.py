
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
    result = []
    for item in library:
        if item['have'] == 1:
            result.append(item)
    return render_template('bookshelf.html', list=result)

@bp.route("/_wish")
def wish_list():
    result = []
    for item in library:
        if item['want'] == 1:
            result.append(item)
    return render_template('wishlist.html', list=result)

@bp.route("/_catalog")
def catalog():
    return render_template('catalog.html', list=library)
 
@bp.route("/<id>")
def list_id(id):
    item = find_by_id(id)
    if len(item) > 0:
        return render_template('catalog.html', list=[item])
    return render_template('catalog.html', list=empty_list(id, "Item does not exist"))

def find_by_id(id):
    if isinstance(id, str):
        id = int(id)

    for item in library:
        if item['id'] == id:
            return item
    return {}

@bp.route("_have/<id>")
def have(id):
    item = find_by_id(id)
    if len(item) > 0:
        item['have'] = 1
        item['want'] = 0
        save_library()
        return id

@bp.route("_want/<id>")
def want(id):
    item = find_by_id(id)
    if len(item) > 0:
        item['have'] = 0
        item['want'] = 1
        save_library()
        return id

@bp.route("_reset/<id>")
def reset(id):
    item = find_by_id(id)
    if len(item) > 0:
        item['have'] = 0
        item['want'] = 0
        save_library()
        return id

@bp.route("/_search/<query>")
def search(query):
    results = []
    q = query.lower()
    for i in library:
        if q in i['title'].lower():
            results.append(i)
    return render_template('search.html', list=results)

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

@bp.route("/_update")
def check_for_update():
    load_catalog()

    loa_latest = get_latest_loa_catalog()
    loa_diff = get_list_difference(loa_latest, catalog)

    if len(loa_diff) > 0:
        # loa_latest is authoritative so overwrite the catalog
        overwrite_catalog_with(loa_latest)
        # add new items to library
        update_library_with(loa_diff)
        return render_template('catalog.html', list=loa_diff)

    return render_template('catalog.html', list=empty_list(0, "No Updates Found"))

# List Helpers
def get_list_difference(list1, list2):
    diff = [i for i in list1 + list2 if i not in list1 or i not in list2]
    return diff

def empty_list(id=0, title='NA', link=''):
    return [{'id': id, 'title': title, 'link': link, 'have': 0, 'want': 0}]

def write_list_to_file(lst, fname):
    json.dump(lst, open(fname, 'w'))

def read_list_from_file(fname):
    return json.load(open(fname, 'r'))

# Library helpers
def save_library():
    write_list_to_file(library, app.config['LIBRARY_FILENAME'])
    load_library()

def load_library():
    global library 
    try:
        library = read_list_from_file(app.config['LIBRARY_FILENAME'])
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
            item['have'] = 0
            item['want'] = 0
            library.append(item)
    save_library()


# Catalog helpers
def save_catalog():
    write_list_to_file(catalog, app.config['CATALOG_FILENAME'])
    load_catalog()

def load_catalog():
    global catalog
    try:
        catalog = read_list_from_file(app.config['CATALOG_FILENAME'])
    except:
        catalog = get_latest_loa_catalog()
        save_catalog()

def overwrite_catalog_with(lst):
    write_list_to_file(lst, app.config['CATALOG_FILENAME'])
    load_catalog()
