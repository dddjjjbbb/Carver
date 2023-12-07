from typing import Dict

from .book_service import BookService
from .book_model import GoodReadsBook


def build_book_model(goodreads_book: GoodReadsBook) -> Dict:
    book_service = BookService(goodreads_book)
    return book_service.build_book_model()

