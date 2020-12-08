
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
            return i
    return "id {} not found".format(id)

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
    return jsonify(results)

@bp.route("/list")
def list():
    return jsonify(library)

@bp.route("/update")
def check_for_update():
    ''' webscrape to create a list of LoA titles '''
    import requests
    from bs4 import BeautifulSoup  
    url = 'https://loa.org/books/loa_collection'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    books = soup.find_all('li', class_='content-listing--book')
    loa_new = []

    for book in books:
        id = int(book.find('i', class_='book-listing__number').text)
        title = book.find('b', class_='content-listing__title').text
        book = {"id": id, "title": title}
        loa_new.append(book)

    loa_old = json.load(open('./loa/loa.json', 'r'))
    loa_diff = [i for i in loa_new + loa_old if i not in loa_new or i not in loa_old]

    message = "No updates, {} records".format(len(loa_new))
    if len(loa_diff) > 0:
        message = "Found {} new records {}".format(len(loa_diff), loa_diff)
        # loa_new is authoritative so overwrite 
        json.dump(loa_new, open('./loa/loa.json', 'w'))
        for i in loa_diff:
            add(i['id'], i['title'])

    return message

def add(id, title):
    library.append({'id': id, 'title': title, 'have': 0, 'want': 0})
    save_library()

def save_library():
    json.dump(library, open('./loa/library.json', 'w'))
    load_library()

def load_library():
    global library 
    library = json.load(open('./loa/library.json', 'r'))
    
load_library()