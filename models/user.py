from itertools import count
import json
from turtle import title
import datetime

class User:
    def __init__(self,id,name,checked_out_books = [], subscribed_to_books = []):
        self._id = id
        self._name = name
        self._checked_out_books = checked_out_books
        self._subscribed_to_books = subscribed_to_books

    def __init__(self, dict):
        self._id = dict['id']
        self._name = dict['name']
        self._checked_out_books = json.loads(dict['checked_out_books'])
        self._subscribed_to_books = json.loads(dict['subscribed_to_books'])

    def name(self):
        return self._name
    
    def id(self):
        return self._id

    def checked_out_books(self):
        return self._checked_out_books

    def subscribed_to_books(self):
        return self._subscribed_to_books
    
    def checkout_book(self, book_isbn):
        self._checked_out_books.append({
            'isbn': book_isbn,
            'checkout_date': datetime.datetime.now().timestamp()
        })

    def subscribe_to_book(self, book_isbn):
        self._subscribed_to_books.append(book_isbn)

    def is_subscribed_to_book(self, book_isbn):
        return book_isbn in self._subscribed_to_books

    def get_book_subscriptions(self):
        return self._subscribed_to_books
    
    def clear_book_subscription(self, book_isbn):
        self._subscribed_to_books.remove(book_isbn)

    def return_book(self, book_isbn):
        filtered_by_isbn = [x for x in self._checked_out_books if x['isbn']== book_isbn]
        if(len(filtered_by_isbn) ==0):
            raise BaseException("Book to return found")
        self._checked_out_books.remove(filtered_by_isbn[0])

    def has_checked_out_book(self, book_isbn):
        return len([x for x in self._checked_out_books if x['isbn'] == book_isbn]) > 0

    def items(self):
        return [
            ('id', self.id()),
            ('name', self.name()),
            ('checked_out_books', json.dumps( self.checked_out_books())), 
            ('subscribed_to_books', json.dumps( self.subscribed_to_books()))
        ]