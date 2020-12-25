from bs4 import BeautifulSoup, ResultSet
from datetime import datetime as dt
from flask import g
import requests
from urllib.parse import urlparse


class LoA(object):

    loa_url = 'https://loa.org/books/loa_collection'
    date_format = '%d-%b-%Y %H:%M:%S'

    def __init__(self, catalog=[], url=loa_url):
        self._catalog = catalog
        self._url = url
        self._last_update = None

    def get_loa(self):
        if 'loa' not in g:
            g.loa = self.get_latest()
        return g.loa

    @property
    def catalog(self):
        return self._catalog

    @catalog.setter
    def catalog(self, val):
        assert(isinstance(val, list))
        self._catalog = val

    @property
    def last_update(self):
        return self._last_update

    @last_update.setter
    def last_update(self, val):
        foo = dt.strptime(val, self.date_format)
        assert(isinstance(foo, dt))
        self._last_update = val

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, val):
        assert(urlparse(val).scheme == "https")
        self._url = val

    @staticmethod
    def sort(lst):
        assert(isinstance(lst, list))
        return sorted(lst, key=lambda i: i['id'])

    def get_latest(self, url=loa_url):
        content = self.loa_request(url)
        books = self.scrape(content)
        self.catalog = self.build_catalog(books, url)
        self.last_update = dt.now().strftime(self.date_format)
        return self.catalog

    @staticmethod
    def loa_request(url=loa_url):
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    @staticmethod
    def scrape(content):
        soup = BeautifulSoup(content, 'html.parser')
        books = soup.find_all('li', class_='content-listing--book')
        if len(books) == 0:
            raise ValueError(
                "Empty results: expected list of books but received none.")
        return books

    def build_catalog(self, books, url=loa_url):
        assert(isinstance(books, ResultSet))
        url_root = "{}://{}".format(
                urlparse(url).scheme, urlparse(url).hostname
            )
        result = []
        for book in books:
            id = int(book.find('i', class_='book-listing__number').text)
            title = book.find('b', class_='content-listing__title').text
            link = url_root + book.find('a')['href']
            book = {"id": id, "title": title, "link": link}
            result.append(book)
        return self.sort(result)
