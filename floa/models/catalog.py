
from bs4 import BeautifulSoup 
import json
import os.path
import requests
from urllib.parse import urlparse

class Catalog(object):
    def __init__(self, *args, **kwargs):
        self._catalog = None
        self._filename = kwargs.get('fname') or None
        self._url = kwargs.get('url') or None
        self._app = kwargs.get('app') or None

        if self._app is not None:
            self._filename = os.path.join(
                        os.path.dirname(self._app.instance_path), 
                        self._app.config['CATALOG_FILENAME'])
            self._url = self._app.config['LOA_COLLECTION_URL']

    @property
    def catalog(self):
        return self._catalog

    @catalog.setter
    def catalog(self, val):
        assert(isinstance(val, list))
        self._catalog = val

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, val):
        assert(isinstance(val, str))
        self._filename = val

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, val):
        assert(isinstance(val, str))
        self._url = val
        return self._url

    def load(self, fname=None):
        if fname is None:
            fname = self._filename
        with open(fname, 'r') as f:
            self._catalog = json.load(f)
        return len(self._catalog)

    def save(self, fname=None):
        if fname is None:
            fname = self._filename
        with open(fname, 'w') as f:
            json.dump(self._catalog, f)
        return len(self._catalog)

    @staticmethod
    def compare(list1, list2):
        assert(isinstance(list1, list))
        assert(isinstance(list2, list))
        diff = [i for i in list1 + list2 if i not in list1 or i not in list2]
        return diff

    def get_latest(self, url=None):
        if url is None:
            url = self._url
        ''' webscrape to create a list of LoA titles ''' 
        urlroot = "{}://{}".format(urlparse(url).scheme, urlparse(url).hostname)
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')
        books = soup.find_all('li', class_='content-listing--book')
        result = []

        for book in books:
            id = int(book.find('i', class_='book-listing__number').text)
            title = book.find('b', class_='content-listing__title').text
            link =  urlroot + book.find('a')['href']
            book = {"id": id, "title": title, "link": link}
            result.append(book)
        return result
