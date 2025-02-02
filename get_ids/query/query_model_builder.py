import re
import urllib
from typing import Union

from get_ids.models.query_model import QueryModel


def build_query_model(query: str, delimiter: str) -> QueryModel:
    book_title = _split_on_last_delimiter(query, delimiter)[0]
    author_name = _split_on_last_delimiter(query, delimiter)[1]

    if _is_subtitle_in_book_title(book_title):
        book_title_minus_subtitle = _remove_subtitle_from_book_title(book_title)
    else:
        book_title_minus_subtitle = None

    return QueryModel(
        book_title=book_title,
        author_name=author_name,
        book_title_minus_subtitle=book_title_minus_subtitle,
        book_title_and_author_name_search_url=_build_search_url_from_query(query),
        book_title_search_url=_build_search_url_from_query(book_title),
        book_title_minus_subtitle_search_url=_build_search_url_from_query(
            book_title_minus_subtitle
        ),
    )


def _split_on_last_delimiter(query: str, delimiter: str) -> [str]:
    return query.rsplit(delimiter, 1)


def _is_subtitle_in_book_title(book_title: str) -> bool:
    subtitles = [": ", "; ", " ("]
    if any(subtitle in book_title for subtitle in subtitles):
        return True
    return False


def _remove_subtitle_from_book_title(book_title: str) -> str:
    subtitle_pattern = re.compile(r"(:|;|\s\().+")
    return re.sub(subtitle_pattern, "", book_title)


def _build_search_url_from_query(query: Union[str, None]) -> Union[str, None]:
    if query is None:
        return None

    if "." in query:
        base_url = "https://www.goodreads.com/search?q="
        return f"{base_url}{urllib.parse.quote(query)}"

    else:
        split_query = _split_on_number(query)
        prefix = _build_new_format_url(split_query)
        base_url = "https://www.goodreads.com/search?q="
        return f"{base_url}{urllib.parse.quote(prefix)}"


def _split_on_number(query: str):
    match = re.match(r"([0-9]+)(.+)", query, re.I)
    if match:
        items = match.groups()
        return items
    return None


def _build_new_format_url(split_query: tuple):
    prefix = f"{split_query[0]}."
    suffix = split_query[1].split("-")[1:]
    return f"{prefix}{'_'.join(suffix)}"
