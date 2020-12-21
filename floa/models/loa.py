from tests.config import LOA_COLLECTION_URL
from bs4 import BeautifulSoup 
import requests
from urllib.parse import urlparse

class LoA(object):
    
    loa_url=LOA_COLLECTION_URL
    
    def __init__(self, *args, **kwargs):
        self._url = kwargs.get('url') or self.loa_url

    @property
    def url(self):
        return self._url

    @staticmethod
    def sort(lst):
        assert(isinstance(lst, list))
        return sorted(lst, key = lambda i: i['id'])

    @classmethod
    def get_latest(cls, url=loa_url):
        content = cls.loa_request(url)
        books = cls.scrape(content)
        catalog = cls.build_catalog(books, url)
        return catalog

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
            raise ValueError("Empty results: expected list of books but received none.")
        return books

    @classmethod
    def build_catalog(cls, books, url=loa_url):
        url_root = "{}://{}".format(urlparse(url).scheme, urlparse(url).hostname)
        result = []
        for book in books:
            id = int(book.find('i', class_='book-listing__number').text)
            title = book.find('b', class_='content-listing__title').text
            link =  url_root + book.find('a')['href']
            book = {"id": id, "title": title, "link": link}
            result.append(book)
        return cls.sort(result)