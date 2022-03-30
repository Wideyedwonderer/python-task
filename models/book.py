from itertools import count
from turtle import title

from utils import isValidISBN


class Book:
    def __init__(self,isbn,title,pages,count):
        if not isValidISBN(isbn):
            raise  BaseException('Please provide valid 10 digit ISBN')
        if pages < 1:
            raise BaseException("Book pages can't be less than 1")

        if count < 1:
            raise BaseException("Book count can't be less than 1")

        self._title = title
        self._pages = pages
        self._isbn = isbn
        self._count = count
        self._available_count = count

    def count(self):
        return self._count
    
    def isbn(self):
        return self._isbn

    def title(self):
        return self._title

    def pages(self):
        return self._pages

    def available_count(self):
        return self._available_count

    def items(self):
        return [('count', self.count()),('title', self.title()),('pages', self.pages()),(('available_count'), self.available_count())]