
from bs4 import BeautifulSoup 
import datetime as dt
import os.path
import pickle
import requests
from urllib.parse import urlparse

class Catalog(object):
    def __init__(self, app, *args, **kwargs):
        self._catalog = []
        self._filename = kwargs.get('fname') or None
        self._url = kwargs.get('url') or None
        self._last_update = None

        if app:
            self._filename = os.path.join(
                        os.path.dirname(app.instance_path), 
                        app.config['CATALOG_FILENAME'])
            self._url = app.config['LOA_COLLECTION_URL']

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

    @property
    def last_update(self):
        return self._last_update

    @last_update.setter
    def last_update(self, val):
        assert(isinstance(val, dt.datetime))
        self._last_update = val
    
    def load(self, fname=None):
        if fname is None:
            fname = self._filename
        if os.path.exists(fname):
            with open(fname, 'rb') as f:
                p = pickle.load(f)
                self.__dict__.clear()
                self.__dict__.update(p.__dict__) 
        return self
         
    def save(self, fname=None):
        if fname is None:
            fname = self._filename
        if not os.path.exists(os.path.dirname(fname)):
            os.makedirs(os.path.dirname(fname))
        with open(fname, 'wb') as f:
            self._last_update = dt.datetime.now().strftime('%d-%b-%Y %H:%M:%S')
            pickle.dump(self, f)
        return self

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
