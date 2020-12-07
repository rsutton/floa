
import json

def init():
    ''' webscrape to create a list of LoA titles '''
    import requests
    from bs4 import BeautifulSoup  
    url = 'https://loa.org/books/loa_collection'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    books = soup.find_all('li', class_='content-listing--book')
    library = []

    for book in books:
        id = int(book.find('i', class_='book-listing__number').text)
        # fixup punctuation characters
        title = book.find('b', class_='content-listing__title').text.encode('iso-8859-1', 'replace').decode('ascii').replace('?', '-')
        book = {"id": id, "title": "{}".format(title)}

        library.append(book)

    with open('loa.json', 'w') as outfile:
        json.dump(library, outfile, indent=4)

def find_by_id(id):
    for i in library:
        if i['id'] == id:
            break
    return i

def have(id):
    item = find_by_id(id)
    item['have'] = 1
    item['want'] = 0
    print(item)

def want(id):
    item = find_by_id(id)
    item['have'] = 0
    item['want'] = 1
    print(item)

def add(id, title):
    library.append({'id': id, 'title': title, 'have': 0, 'want': 0})

def save():
    json.dump(library, open('library.json', 'w'))

# library.json is the annotated version of loa.json
# containing 'have' and 'want' fields
library = json.load(open('library.json', 'r'))

