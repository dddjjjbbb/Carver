import re
import urllib
from typing import Union

from get_ids.models.query_model import QueryModel
from src.book_id.query.query_config import *


class QueryService:
    def __init__(self, query: Union[str, None]):
        self.query = query

    def build_query_model(self) -> Union[QueryModel, IndexError]:
        try:
            book_title = QueryService._split_on_last_delimiter(self)[0]
            author_name = QueryService._split_on_last_delimiter(self)[1]

        except IndexError as e:
            raise IndexError(f"Please check if the delimiter is present and as specified. See: {e}")

        search_query = f"{book_title} - {author_name}"

        if QueryService._is_subtitle_in_book_title(book_title):
            book_title_minus_subtitle = QueryService._remove_subtitle_from_book_title(book_title)
        else:
            book_title_minus_subtitle = None

        return QueryModel(
            book_title=book_title,
            author_name=author_name,
            book_title_minus_subtitle=book_title_minus_subtitle,
            book_title_and_author_name_search_url=QueryService._build_search_url_from_query(search_query),
            book_title_search_url=QueryService._build_search_url_from_query(book_title),
            book_title_minus_subtitle_search_url=QueryService._build_search_url_from_query(book_title_minus_subtitle),
        )

    def _split_on_last_delimiter(self) -> [str]:
        split = self.query.rsplit(config_delimiter, 1)
        return [query.strip() for query in split]

    @staticmethod
    def _is_subtitle_in_book_title(book_title: str) -> bool:
        subtitles = [": ", "; ", " ("]
        if any(subtitle in book_title for subtitle in subtitles):
            return True
        return False

    @staticmethod
    def _remove_subtitle_from_book_title(book_title: str) -> str:
        subtitle_pattern = re.compile(r"(:|;|\s\().+")
        return re.sub(subtitle_pattern, "", book_title)

    @staticmethod
    def _build_search_url_from_query(query: str) -> Union[str, None]:
        if query is None:
            return None

        base_url = "https://www.goodreads.com/search?q="
        return f"{base_url}{urllib.parse.quote(query)}"
