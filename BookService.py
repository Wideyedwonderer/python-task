import Persistance
from models.book import Book
from models.collectionsEnum import PersistanceCollections
from models.user import User


def add_new_book(isbn, title, pages, count):

    book = Book(isbn, title, int(pages), int(count))
    Persistance.persist_by_id(isbn, PersistanceCollections.BOOKS.value, book)

def remove_book(book_isbn):

    try:    
         Persistance.get_by_id(book_isbn, PersistanceCollections.BOOKS.value)
    except:
         raise BaseException('Book not found')
    Persistance.remove_by_id(book_isbn, PersistanceCollections.BOOKS.value)

def checkout_book(user_id, book_isbn):
    if not _is_book_available(book_isbn):
        raise BaseException('Book is not available. Try reserving it instead.')

    book = Persistance.get_by_id(book_isbn, PersistanceCollections.BOOKS.value)
    user = User(Persistance.get_by_id(
        user_id, PersistanceCollections.USERS.value))

    if user.has_checked_out_book(book_isbn):
        raise BaseException('Book already checked out.')

    book['available_count'] = str(int(book['available_count']) - 1)
    Persistance.persist_by_id(
        book_isbn, PersistanceCollections.BOOKS.value, book)

    user.checkout_book(book_isbn)
    Persistance.persist_by_id(
        user_id, PersistanceCollections.USERS.value, user)

def return_book(user_id, book_isbn):
    book = Persistance.get_by_id(book_isbn, PersistanceCollections.BOOKS.value)
    user = User(Persistance.get_by_id(
        user_id, PersistanceCollections.USERS.value))

    if not user.has_checked_out_book(book_isbn):
        raise BaseException('Book has not been checked out.')

    user.return_book(book_isbn)
    book['available_count'] = str(int(book['available_count']) + 1)
    Persistance.persist_by_id(
        user_id, PersistanceCollections.USERS.value, user)

    Persistance.persist_by_id(
        book_isbn, PersistanceCollections.BOOKS.value, book)

def subscribe_to_book(user_id, book_isbn):
    if _is_book_available(book_isbn):
        raise BaseException("Can't subscribe to book that is currently available.")

    user = User(Persistance.get_by_id(
        user_id, PersistanceCollections.USERS.value))

    if user.is_subscribed_to_book(book_isbn):
        raise BaseException('Book has already been subscribed to.')

    user.subscribe_to_book(book_isbn)
    Persistance.persist_by_id(
        user_id, PersistanceCollections.USERS.value, user)


def print_notifications_for_subscribed_books():
    user_ids = list(map(lambda id: int(id), Persistance.get_all_ids_from_collection(
        PersistanceCollections.USERS.value)))
    available_books_isbns = _get_available_books_isbns()

    for user_id in user_ids:
        user = User(Persistance.get_by_id(
            user_id, PersistanceCollections.USERS.value))
        subscriptions = user.get_book_subscriptions()

        for subscription in subscriptions:
            if subscription in available_books_isbns:
                print('Book with isbn ' + str(subscription) +
                      ' has recently become available to be rented by subscriber ' + user.name())
                user.clear_book_subscription(subscription)
                Persistance.persist_by_id(
                    user.id(), PersistanceCollections.USERS.value, user)


def is_book_available(book_isbn):
    return 'Book is available' if _is_book_available(book_isbn) else 'Book is not availaable'


def _get_available_books_isbns():
    return [x for x in _get_book_isbns() if _is_book_available(x)]


def _is_book_available(book_isbn):
    book_available_count = int(Persistance.get_field(
        book_isbn, PersistanceCollections.BOOKS.value, 'available_count'))
    return book_available_count > 0


def _get_book_isbns():
    return list(map(lambda id: id, Persistance.get_all_ids_from_collection(PersistanceCollections.BOOKS.value)))
