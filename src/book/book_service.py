import logging
import math
import re
from typing import Dict, Union

import bs4
import gender_guesser.detector as gender
from nameparser.parser import HumanName

from src.author.author_controller import build_author_model
from src.book.book_config import *
from src.common.errors.errors import (return_none_for_attribute_error,
                                      return_none_for_index_error,
                                      return_none_for_type_error)
from src.common.formatters.json.to_json import to_json
from src.common.network.network import get
from src.common.parser.parser import parse
from src.common.utils.dict_operators import sort_by_value
from src.common.utils.string_operators import split_on_delimiter

from ..common.errors.errors import return_none_for_value_error
from .book_model import BookModel, GoodReadsBook

d = gender.Detector()


class BookService:
    def __init__(self, goodreads_book: GoodReadsBook):
        self.goodreads_book = goodreads_book

    def build_book_model(self):
        logging.info(f"Building model for: '{self.goodreads_book.id}'")
        BASE_URL = "https://www.goodreads.com/book/show/"
        url = f"{BASE_URL}{self.goodreads_book.id}"

        # BOOK
        book_response = get(url)
        book_soup = parse(book_response)
        good_reads_book_parser = GoodReadsBookParser(book_soup)

        year_of_publication = good_reads_book_parser.get_year_of_publication()
        author_full_name = (
            good_reads_book_parser.get_author_full_name()
            if config_author_full_name is True
            else None
        )
        if author_full_name:
            print(author_full_name)
        else:
            print("COULD NOT GET AUTHOR")
        genres = good_reads_book_parser.get_genres()
        title = good_reads_book_parser.get_title()

        # FIGURE OUT WHAT IS WRONG HERE!

        try:
            author_model = build_author_model(author_full_name)
        except Exception as e:
            print(f"AUTHOR MODEL EXCEPTION: {e}")
            author_model = None

        try:
            country_of_citizenship = author_model.country_of_citizenship
            gender = author_model.gender
        except AttributeError:
            country_of_citizenship = ""
            gender = d.get_gender(
                good_reads_book_parser.get_author_first_name(author_full_name).title()
            )

        book_model = BookModel(
            title=good_reads_book_parser.get_title() if config_title is True else None,
            author_full_name=author_full_name,
            isbn=good_reads_book_parser.get_isbn() if config_isbn is True else None,
            isbn13=good_reads_book_parser.get_isbn13()
            if config_isbn13 is True
            else None,
            author_last_name=good_reads_book_parser.get_author_last_name(
                author_full_name
            )
            if config_author_last_name is True
            else None,
            author_first_name=good_reads_book_parser.get_author_first_name(
                author_full_name
            )
            if config_author_first_name is True
            else None,
            year_of_publication=good_reads_book_parser.get_year_of_publication()
            if config_year_of_publication is True
            else None,
            century_of_publication=good_reads_book_parser.get_century_of_publication(
                year_of_publication
            )
            if config_century_of_publication is True
            else None,
            genre=good_reads_book_parser.get_primary_genre(genres)
            if config_primary_genre is True
            else None,
            number_of_pages=good_reads_book_parser.get_number_of_pages()
            if config_number_of_pages is True
            else None,
            average_rating=good_reads_book_parser.get_average_rating()
            if config_average_rating is True
            else None,
            goodreads_url=good_reads_book_parser.construct_goodreads_url(
                self.goodreads_book.id
            )
            if config_goodreads_url is True
            else None,
            author_country_of_citizenship=country_of_citizenship
            if country_of_citizenship is True
            else None,
            author_gender=gender,
            number_of_ratings=good_reads_book_parser.get_number_of_ratings()
            if config_number_of_ratings is True
            else None,
            number_of_reviews=good_reads_book_parser.get_number_of_reviews()
            if config_number_of_reviews is True
            else None,
            series_name=good_reads_book_parser.get_series_name()
            if config_series_name is True
            else None,
            series_url=good_reads_book_parser.get_series_url()
            if config_series_url is True
            else None,
            shelves="" if config_shelves is True else None,
            title_id=self.goodreads_book.id if config_title_id is True else None,
            lists=None,
            numeric_id=good_reads_book_parser.get_numeric_id(self.goodreads_book.id)
            if config_numeric_id is True
            else None,
            rating_distribution=None if config_rating_distribution is True else None,
        )

        model = book_model
        return to_json(model)


class GoodReadsBookParser:
    def __init__(self, soup: bs4.BeautifulSoup):
        self.soup = soup

    @staticmethod
    def get_numeric_id(book_id_title: str) -> [int, None]:
        try:
            return int(split_on_delimiter(book_id_title, "."))
        except ValueError:
            return int(split_on_delimiter(book_id_title, "-"))

    @return_none_for_attribute_error
    def get_title(self) -> str:
        title = self.soup.find("h1", {"class": "Text__title1"}).text.strip()
        return title

    def get_author_full_name(self):
        author_links = self.soup.find_all("a", {"class": "ContributorLink"})

        for link in author_links:
            full_name_element = link.find("span", {"class": "ContributorLink__name"})
            if full_name_element:
                full_name = full_name_element.text.strip()
                if full_name:
                    try:
                        return full_name.encode("ISO-8859-1").decode("utf-8")
                    except UnicodeDecodeError as e:
                        return None
                return None
        return None

    @staticmethod
    def get_author_first_name(author_full_name: str) -> str:
        if author_full_name:
            return HumanName(author_full_name).first
        return ""

    @staticmethod
    def get_author_last_name(author_full_name: str) -> str:
        if author_full_name:
            return HumanName(author_full_name).last
        return ""

    @return_none_for_attribute_error
    @return_none_for_value_error
    def get_number_of_pages(self) -> Union[int, None]:
        num_pages = self.soup.find("p", {"data-testid": "pagesFormat"}).text.strip()

        if "ebook" in num_pages:
            return None
        return int(num_pages.split()[0])

    @return_none_for_attribute_error
    def get_year_of_publication(self) -> int:
        year_of_publication = self.soup.find(
            "p", attrs={"data-testid": "publicationInfo"}
        ).string.strip()
        return int(re.search("([0-9]{3,4})", year_of_publication).group())

    @staticmethod
    @return_none_for_type_error
    def get_century_of_publication(year_of_publication: int) -> int:
        return math.ceil(year_of_publication / 100)

    @return_none_for_attribute_error
    def get_genres(self) -> [str]:
        # Button Button--tag-inline Button--small
        # TODO: It might be nice build a list of dicts considering the votes here.
        genres = self.soup.find_all(
            "a", {"class": "Button Button--tag-inline Button--small"}
        )
        return [a.text.strip() for a in genres]

    @staticmethod
    @return_none_for_index_error
    @return_none_for_type_error
    def get_primary_genre(genres: [str]) -> str:
        return genres[0]

    @return_none_for_attribute_error
    def get_series_name(self) -> str:
        book_series_name = self.soup.find(
            "h3",
            {"class": "Text Text__title3 Text__italic Text__regular Text__subdued"},
        ).text.strip()
        return book_series_name

    @return_none_for_attribute_error
    @return_none_for_type_error
    def get_series_url(self) -> str:
        h3 = self.soup.find_all(
            "h3",
            {"class": "Text Text__title3 Text__italic Text__regular Text__subdued"},
        )
        for node in h3:
            uri = node.find("a")["href"]
            return uri

    @return_none_for_index_error
    def get_isbn(self) -> int:
        isbn = re.search('("isbn":")([0-9]{10})', str(self.soup))

        if isbn:
            return int(isbn.group(2))
        return 1

    # @return_none_for_index_error
    def get_isbn13(self) -> int:
        # (contentContainer">)([0-9]{13})
        isbn13 = re.search(r'("isbn13":")([0-9]{13})', str(self.soup))

        if isbn13:
            return int(isbn13.group(2))
        return 1

    def get_lists_url(self, book_id_title) -> str:
        list_url = "https://www.goodreads.com/list/book/"

        if book_id_title is None:
            return None

        numeric_id = str(self.get_numeric_id(book_id_title))
        return f"{list_url}{numeric_id}"

    @return_none_for_type_error
    @return_none_for_attribute_error
    @return_none_for_value_error
    def get_number_of_reviews(self) -> Union[int, None]:
        value = self.soup.find("span", {"data-testid": "reviewsCount"}).text.strip()

        if "reviews" in value:
            value = value.replace("\xa0reviews", "")
        else:
            value = value.replace("\xa0review", "")

        value = value.replace(",", "")
        return int(value)

    @return_none_for_type_error
    @return_none_for_attribute_error
    def get_number_of_ratings(self) -> Union[int, None]:
        value = self.soup.find("span", {"data-testid": "ratingsCount"}).text.strip()
        value = value.replace("\xa0ratings", "")
        value = value.replace(",", "")
        if "rating" not in value:
            return int(value)
        return None

    @return_none_for_value_error
    @return_none_for_attribute_error
    def get_average_rating(self) -> Union[float, None]:
        value = self.soup.find(
            "div", {"class": "RatingStatistics__rating"}
        ).text.strip()
        f = float(value)
        return round(f, 2)

    @return_none_for_attribute_error
    def get_rating_distribution(self) -> Dict[str, int]:
        pattern = re.compile(r"\[(\d+),(\d+),(\d+),(\d+),(\d+)\]")

        distribution = re.findall(pattern, str(self.soup))[0]
        distribution = [int(num) for num in distribution]

        result = {
            "fiveStar": distribution[0],
            "fourStar": distribution[1],
            "threeStar": distribution[2],
            "twoStar": distribution[3],
            "oneStar": distribution[4],
        }

        return dict(sort_by_value(result))

    @return_none_for_type_error
    @return_none_for_attribute_error
    def _get_shelves_url(self) -> str:
        match = re.search(
            r'("shelvesUrl":")(https://www.goodreads.com/work/shelves/.+?)(")',
            str(self.soup),
        ).group(2)
        return match

    @staticmethod
    @return_none_for_attribute_error
    def construct_goodreads_url(goodreads_book_id: str) -> str:
        BASE_URL = "https://www.goodreads.com/book/show/"
        book_url = f"{BASE_URL}{goodreads_book_id}"
        libre_hyperlink = f'=HYPERLINK("{book_url}", "Goodreads URL")'
        return libre_hyperlink
