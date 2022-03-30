from lib2to3.pytree import Base
from time import time
from typing import overload
import Persistance
from datetime import timedelta, datetime
from models.collectionsEnum import PersistanceCollections
from models.user import User
from utils import infinite_input
import BookService as BookService


def add_user(name):
    ids = list(map(lambda id: int(id), Persistance.get_all_ids_from_collection(
        PersistanceCollections.USERS.value)))

    id = None
    if len(ids) == 0:
        id = 1
    else:
        last_used_id = ids.pop(len(ids) - 1)
        id = last_used_id + 1

    userToAdd = User({'name': name,'id': id, 'checked_out_books': '[]', 'subscribed_to_books': '[]'})

    Persistance.persist_by_id(
        id, PersistanceCollections.USERS.value, userToAdd)


def remove_user(user_id):
    return_user_books = infinite_input("Return user's books?", ['y', 'n'])

    try:
        user = User(Persistance.get_by_id(
            user_id, PersistanceCollections.USERS.value))
    except KeyError:
        raise BaseException('User not found')

    if return_user_books == 'y':
        for checked_out_book in user.checked_out_books():
            BookService.return_book(user_id, checked_out_book['isbn'])

    Persistance.remove_by_id(user_id, PersistanceCollections.USERS.value)


def get_overdue_books_isbns(user_id):
    return list(map(lambda book: book['isbn'], _get_overdue_books(user_id)))


def get_overdue_fine(user_id, book_isbn):
    return str(_get_overdue_fine_amount_for_book(user_id, book_isbn)) + "$"


def get_book_subscriber_ids(book_isbn):
    user_ids = list(map(lambda id: int(id), Persistance.get_all_ids_from_collection(
        PersistanceCollections.USERS.value)))

    subscribed_users = [
        x for x in user_ids if _is_user_subscribed_to_book(x, book_isbn)]

    return subscribed_users


def get_users_who_checked_out_book(book_isbn):
    user_ids = list(map(lambda id: int(id), Persistance.get_all_ids_from_collection(
        PersistanceCollections.USERS.value)))
    return [x for x in user_ids if _has_user_checked_out_book(x, book_isbn)]


desired_days_overdue_period = 90


def get_total_fine_for_user(user_id):
    total_fine = 0
    overdue_books = _get_overdue_books(user_id)
    for book in overdue_books:
        total_fine += _get_overdue_fine_amount_for_book(user_id, book['isbn'])
    return str(total_fine) + "$"


def _get_overdue_books(user_id):
    user = User(Persistance.get_by_id(
        user_id, PersistanceCollections.USERS.value))
    checked_out_books = user.checked_out_books()
    return [x for x in checked_out_books if _is_date_overdue(x['checkout_date'])]


def _get_overdue_fine_amount_for_book(user_id, book_isbn):
    overdue_books = _get_overdue_books(user_id)
    overdue_books_isbns = list(map(lambda book: book['isbn'], overdue_books))
    if not book_isbn in overdue_books_isbns:
        raise BaseException("Book is not overdue")
    index = overdue_books_isbns.index(book_isbn)

    overdue_amount = _get_overdue_amount(overdue_books[index]['checkout_date'])

    seconds_in_week = 604800
    overdue_weeks = int(overdue_amount) // seconds_in_week

    return overdue_weeks * 5


def _is_date_overdue(timestamp):

    overdue_amount = _get_overdue_amount(timestamp)
    return overdue_amount >= 0


def _get_overdue_amount(checkout_timestamp):
    checkout_date = datetime.fromtimestamp(checkout_timestamp)

    desired_return_date = checkout_date + \
        timedelta(days=desired_days_overdue_period)

    now = datetime.now().timestamp()
    return now - desired_return_date.timestamp()


def _is_user_subscribed_to_book(user_id, book_isbn):
    user = User(Persistance.get_by_id(
        user_id, PersistanceCollections.USERS.value))
    return user.is_subscribed_to_book(book_isbn)


def _has_user_checked_out_book(user_id, book_isbn):
    user = User(Persistance.get_by_id(
        user_id, PersistanceCollections.USERS.value))
    return user.has_checked_out_book(book_isbn)
