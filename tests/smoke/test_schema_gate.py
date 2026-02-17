import json
import re
from pathlib import Path

import pytest
import requests
from bs4 import BeautifulSoup

SCHEMA_PATH = Path(__file__).parent.parent.parent / "schema" / "expected_selectors.json"


@pytest.fixture(scope="module")
def schema():
    with open(SCHEMA_PATH) as f:
        return json.load(f)


@pytest.fixture(scope="module")
def book_page(schema):
    url = schema["book_page"]["url"]
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


class TestBookPageSelectors:
    @pytest.fixture(autouse=True)
    def _setup(self, schema, book_page):
        self.selectors = schema["book_page"]["selectors"]
        self.patterns = schema["book_page"]["patterns"]
        self.soup = book_page

    @pytest.mark.parametrize(
        "selector_name",
        [
            "title",
            "author_link",
            "author_name",
            "pages_format",
            "publication_info",
            "genres",
            "reviews_count",
            "ratings_count",
            "average_rating",
            "json_ld",
        ],
    )
    def test_selector_finds_elements(self, selector_name):
        selector = self.selectors[selector_name]
        elements = self.soup.find_all(selector["tag"], selector["attrs"])
        assert len(elements) > 0, (
            f"Selector '{selector_name}' found nothing. "
            f"Goodreads may have changed their HTML. "
            f"Looking for: <{selector['tag']}> with {selector['attrs']}"
        )

    @pytest.mark.parametrize("pattern_name", ["rating_distribution", "shelves_url"])
    def test_regex_pattern_matches(self, pattern_name):
        pattern_info = self.patterns[pattern_name]
        matches = re.findall(pattern_info["regex"], str(self.soup))
        assert len(matches) > 0, (
            f"Pattern '{pattern_name}' found no matches. "
            f"Goodreads may have changed their page structure. "
            f"Regex: {pattern_info['regex']}"
        )

    def test_json_ld_contains_expected_fields(self):
        script = self.soup.find("script", type="application/ld+json")
        assert script is not None, "No JSON-LD script tag found"
        data = json.loads(script.string)
        for field in ["name", "numberOfPages", "aggregateRating"]:
            assert field in data, f"JSON-LD missing expected field: {field}"
