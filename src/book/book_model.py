from dataclasses import dataclass
from typing import Dict, Optional, Union

from dataclasses_json.api import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GoodReadsBook:
    id: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class BookModel:

    title: Union[str, None]
    author_full_name: Union[str, None]
    isbn: Union[str, None]
    isbn13: Union[str, None]
    author_last_name: Union[str, None]
    author_first_name: Union[str, None]
    year_of_publication: Union[int, None]
    century_of_publication: Union[int, None]
    genre: Union[str, None]
    number_of_pages: Union[int, None]
    average_rating: Union[float, None]
    goodreads_url: Union[str, None]
    first_edition_hardback_cost_in_uk: Union[str, None]
    abe_books_search_url: Union[str, None]
    author_country_of_citizenship: Union[str, None]
    author_gender: Union[str, None]
    number_of_ratings: Union[int, None]
    number_of_reviews: Union[int, None]
    series_name: Union[str, None]
    series_url: Union[str, None]
    shelves: Union[Dict, None]
    title_id: Union[str, None]
    lists: Union[str, None]
    numeric_id: Union[int, None]
    rating_distribution: Union[Dict, None]