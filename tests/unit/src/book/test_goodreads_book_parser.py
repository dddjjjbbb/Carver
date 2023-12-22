import pytest
from data.all_the_pretty_horses import all_the_pretty_horses_soup
from data.empty import empty_soup

from src.book.book_service import GoodReadsBookParser
from tests.unit.src.book.data.cronopios_and_famas import \
    cronopios_and_famas_soup


class TestBookService:
    def setup_method(self):
        self.book_id_title = "469571.All_the_Pretty_Horses"
        self.book_id_title_without_decimal = "13079982-fahrenheit-451"
        self.goodreads_book_parser = GoodReadsBookParser(all_the_pretty_horses_soup)
        self.goodreads_book_parser_empty = GoodReadsBookParser(empty_soup)
        self.shelf = "to-read 61,056 people"

    def test_get_numeric_book_id(self):
        assert self.goodreads_book_parser.get_numeric_id(self.book_id_title) == 469571

    def test_get_numeric_book_id_where_no_decimal_is_present(self):
        assert (
            self.goodreads_book_parser.get_numeric_id(
                self.book_id_title_without_decimal
            )
            == 13079982
        )

    def test_get_book_title(self):
        assert self.goodreads_book_parser.get_title() == "All the Pretty Horses"

    def test_get_book_title_should_return_none_where_soup_find_fails(self):
        assert self.goodreads_book_parser_empty.get_title() is None

    def test_get_book_series_name(self):
        assert self.goodreads_book_parser.get_series_name() == "The Border Trilogy #1"

    def test_get_book_series_name_should_return_none_where_soup_find_fails(self):
        assert self.goodreads_book_parser_empty.get_series_name() is None

    def test_get_book_series_url(self):
        assert (
            self.goodreads_book_parser.get_series_url()
            == "https://www.goodreads.com/series/44780-the-border-trilogy"
        )

    def test_get_book_series_url_should_return_none_where_soup_find_fails(self):
        assert self.goodreads_book_parser_empty.get_series_url() is None

    def test_get_isbn(self):
        assert self.goodreads_book_parser.get_isbn() == 9780679744

    def test_get_isbn_should_return_none_where_soup_findall_fails(self):
        assert self.goodreads_book_parser_empty.get_isbn() == 1

    def test_get_isbn13(self):
        assert self.goodreads_book_parser.get_isbn13() == 9780679744399

    def test_get_isbn13_should_return_none_where_soup_findall_fails(self):
        assert self.goodreads_book_parser_empty.get_isbn() == 1

    def test_get_lists_url(self):
        assert (
            self.goodreads_book_parser.get_lists_url(self.book_id_title)
            == "https://www.goodreads.com/list/book/469571"
        )

    def test_get_lists_url_should_return_none_where_soup_find_fails(self):
        assert (
            self.goodreads_book_parser_empty.get_lists_url(self.book_id_title) is None
        )

    def test_get_year_of_publication(self):
        assert self.goodreads_book_parser.get_year_of_publication() == 1992

    def test_get_year_of_publication_should_return_none_where_soup_find_fails(self):
        assert self.goodreads_book_parser_empty.get_year_of_publication() is None

    def test_get_author_full_name(self):
        goodreads_book_parser = GoodReadsBookParser(all_the_pretty_horses_soup)
        assert goodreads_book_parser.get_author_full_name() == "Cormac McCarthy"

    def test_get_author_full_name_where_multiple_authors_listed(self):
        goodreads_book_parser = GoodReadsBookParser(cronopios_and_famas_soup)
        assert goodreads_book_parser.get_author_full_name() == "Julio Cortázar"
        # Julio CortÃ¡zar

    def test_get_author_full_name_should_return_none_where_soup_find_fails(self):
        assert self.goodreads_book_parser_empty.get_author_full_name() is None

    full_names_to_first_names = [
        ("Cormac McCarthy", "Cormac"),
        ("Jean-Jacques Rousseau", "Jean-Jacques"),
        ("G.A. Cohen", "G.A."),
        ("Olav H. Hauge", "Olav"),
        ("P.M.", "P.M."),
        ("Aeschylus", "Aeschylus"),
    ]

    @pytest.mark.parametrize("full_name, expected", full_names_to_first_names)
    def test_get_author_first_name(self, full_name, expected):
        assert self.goodreads_book_parser.get_author_first_name(full_name) == expected

    full_names_to_last_names = [
        ("Cormac McCarthy", "McCarthy"),
        ("Jean-Jacques Rousseau", "Rousseau"),
        ("G.A. Cohen", "Cohen"),
        ("Olav H. Hauge", "Hauge"),
        ("P.M.", ""),
        ("Aeschylus", ""),
    ]

    @pytest.mark.parametrize("full_name, expected", full_names_to_last_names)
    def test_get_author_last_name(self, full_name, expected):
        assert self.goodreads_book_parser.get_author_last_name(full_name) == expected

    def test_get_number_of_pages(self):
        assert self.goodreads_book_parser.get_number_of_pages() == 302

    def test_get_number_of_pages_should_return_none_where_soup_find_fails(self):
        assert self.goodreads_book_parser_empty.get_number_of_pages() is None

    def test_get_genres(self):
        expected = [
            "Fiction",
            "Westerns",
            "Historical Fiction",
            "Classics",
            "Literature",
            "Novels",
            "Literary Fiction",
            "coming-of-age",
            "western",
            "2011",
            "modern-lit",
            "western",
            "classic-novels",
            "mexico",
            "bildungsroman",
            "friendship-and-found-family",
            "landscape-location-protagonist",
            "1001-before-you-die",
            "2018",
            "american",
            "dark",
            "family-ties",
            "favorite-author",
            "fiction-general",
            "western",
            "did-not-finish",
            "disappointing",
            "film",
            "americana",
            "western",
            "historical-fiction",
            "literary-fiction",
            "netgalley",
            "1001-books",
            "american-literature",
            "american-southwest",
            "modern-western",
            "novels",
            "dost",
            "read-in-2019",
            "american-west",
            "best-of-2014",
            "read-2014",
            "xx2018-completed",
            "fiction",
            "government",
            "historical-fiction",
            "library-loan",
            "historical-fiction",
            "2009",
            "atmospheric",
            "award-winner",
            "favorites",
            "5-star",
            "fiction",
            "grit-lit",
            "5-star-books",
            "april-2022",
            "favorites",
            "classics",
            "favorites",
        ]
        assert self.goodreads_book_parser.get_genres() == expected

    def test_get_genres_should_return_none_where_soup_find_fails(self):
        assert self.goodreads_book_parser_empty.get_number_of_pages() is None

    def test_get_primary_genre(self):
        genre_list = [
            "Fiction",
            "Westerns",
            "Historical > Historical Fiction",
            "Classics",
            "Literature",
            "Novels",
            "Literary Fiction",
            "Literature > American",
            "Contemporary",
            "Adventure",
        ]
        assert self.goodreads_book_parser.get_primary_genre(genre_list) == "Fiction"

    def test_get_primary_genre_should_return_none_where_genre_list_is_empty(self):
        assert self.goodreads_book_parser_empty.get_primary_genre() is None

    def test_get_lists_url(self):
        assert (
            self.goodreads_book_parser.get_lists_url(self.book_id_title)
            == "https://www.goodreads.com/list/book/469571"
        )

    def test_get_lists_url_should_return_none_where_soup_find_fails(self):
        assert self.goodreads_book_parser_empty.get_lists_url(None) is None

    def test_get_number_of_reviews(self):
        assert self.goodreads_book_parser.get_number_of_reviews() == 8381

    def test_get_number_of_reviews_should_return_none_where_soup_find_fails(self):
        assert self.goodreads_book_parser_empty.get_number_of_reviews() is None

    def test_get_number_of_ratings(self):
        assert self.goodreads_book_parser.get_number_of_ratings() == 119566

    def test_get_number_of_ratings_should_return_none_where_soup_find_fails(self):
        assert self.goodreads_book_parser_empty.get_number_of_ratings() is None

    def test_get_average_rating(self):
        assert self.goodreads_book_parser.get_average_rating() == 4.03

    def test_get_average_rating_should_return_none_where_soup_find_fails(self):
        assert self.goodreads_book_parser_empty.get_average_rating() is None

    def test_get_rating_distribution(self):
        expected = {
            "fiveStar": 2051,
            "fourStar": 5479,
            "oneStar": 42546,
            "threeStar": 21678,
            "twoStar": 47812,
        }
        assert self.goodreads_book_parser.get_rating_distribution() == expected

    def test_get_rating_distribution_should_return_none_where_soup_find_fails(self):
        assert self.goodreads_book_parser_empty.get_average_rating() is None

    def test_get_shelves_url(self):
        assert (
            self.goodreads_book_parser._get_shelves_url()
            == "https://www.goodreads.com/work/shelves/1907621-all-the-pretty-horses"
        )

    def test_get_shelves_url_should_return_none_where_soup_find_fails(self):
        assert self.goodreads_book_parser_empty._get_shelves_url() is None

    def test_get_century_of_publication(self):
        assert self.goodreads_book_parser.get_century_of_publication(1992) == 20
