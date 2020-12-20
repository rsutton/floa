from bs4 import BeautifulSoup 
import requests
from urllib.parse import urlparse

class LoA(object):

    loa_url = 'https://loa.org/books/loa_collection'

    def __init__(self, *args, **kwargs):
        self._url = kwargs.get('url') or self.loa_url
        
    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, val):
        assert(isinstance(val, str))
        self._url = val
        return self._url

    @staticmethod
    def sort(lst):
        assert(isinstance(lst, list))
        return sorted(lst, key = lambda i: i['id'])

    def get_latest(self, url=None):
        if url is None:
            url = self.url
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
        return self.sort(result)
