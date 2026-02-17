from src.book_id.query.query_controller import build_query_model
from src.book_id.query.query_model import QueryModel


class TestQueryController:
    def setup_method(self):
        self.query_with_single_delimiter = "Kitchen - Banana Yoshimoto"
        self.query_with_multiple_delimiters = "63, Dream Palace: Selected Stories, 1956-1987 - James Purdy"

    def test_build_query_model_should_return_a_query_model_where_book_title_does_not_contain_a_subtitle(
        self,
    ):
        query_model = QueryModel(
            book_title="Kitchen",
            author_name="Banana Yoshimoto",
            book_title_minus_subtitle=None,
            book_title_and_author_name_search_url="https://www.goodreads.com/search?q=Kitchen%20-%20Banana%20Yoshimoto",
            book_title_search_url="https://www.goodreads.com/search?q=Kitchen",
            book_title_minus_subtitle_search_url=None,
        )

        result = build_query_model(self.query_with_single_delimiter)
        assert result.book_title == query_model.book_title
        assert result.author_name == query_model.author_name
        assert result.book_title_minus_subtitle == query_model.book_title_minus_subtitle
        assert result.book_title_and_author_name_search_url == query_model.book_title_and_author_name_search_url
        assert result.book_title_search_url == query_model.book_title_search_url
        assert result.book_title_minus_subtitle_search_url == query_model.book_title_minus_subtitle_search_url

    def test_it_build_query_model_should_return_a_query_model_where_book_title_contains_a_subtitle(
        self,
    ):
        query_model = QueryModel(
            book_title="63, Dream Palace: Selected Stories, 1956-1987",
            author_name="James Purdy",
            book_title_minus_subtitle="63, Dream Palace",
            book_title_and_author_name_search_url="https://www.goodreads.com/search?q=63%2C%20Dream%20Palace%3A%20Selected%20Stories%2C%201956-1987%20-%20James%20Purdy",
            book_title_search_url="https://www.goodreads.com/search?q=63%2C%20Dream%20Palace%3A%20Selected%20Stories%2C%201956-1987",
            book_title_minus_subtitle_search_url="https://www.goodreads.com/search?q=63%2C%20Dream%20Palace",
        )

        result = build_query_model(self.query_with_multiple_delimiters)
        assert result.book_title == query_model.book_title
        assert result.author_name == query_model.author_name
        assert result.book_title_minus_subtitle == query_model.book_title_minus_subtitle
        assert result.book_title_and_author_name_search_url == query_model.book_title_and_author_name_search_url
        assert result.book_title_search_url == query_model.book_title_search_url
        assert result.book_title_minus_subtitle_search_url == query_model.book_title_minus_subtitle_search_url
