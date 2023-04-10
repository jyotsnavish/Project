import requests
from . import BOOK_API_URL

class BookClient:
    @staticmethod
    def get_books():
        url = BOOK_API_URL + '/api/book/all'
        response = requests.get(url)
        return response.json()
    
    @staticmethod
    def get_book(slug):
        url = BOOK_API_URL + '/api/book/'+slug
        response = requests.get(url)
        return response.json()
    
    @staticmethod
    def get_book_by_id(book_id):
        response = requests.get(BOOK_API_URL + '/api/book/id/' + str(book_id))
        return response.json()