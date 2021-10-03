from typing import Dict

import bs4

from src.common.errors.errors import (return_none_for_index_error,
                                      return_none_for_type_error)
from src.shelf.shelf_config import *


class ShelfService:
    def __init__(self, soup: bs4.BeautifulSoup):

        self.soup = soup
        self.GOODREADS_BASE_URL = "https://www.goodreads.com"

    def get_shelves(self) -> [Dict]:
        #  The amount of results returned is dependent on `config_number_of_shelf_results`

        shelves = []

        for shelf in ShelfService._get_unformatted_shelves(self.soup):
            name = ShelfService._get_shelf_name(shelf)
            count = ShelfService._get_shelf_count(shelf)

            shelves.append(
                {"shelfName": name, "AmountOfUsersWhoAddedBookToList": count}
            )

        return shelves[:config_number_of_shelf_results]

    @return_none_for_type_error
    def _get_shelves_url(self):
        shelves_url = self.soup.find("a", text="See top shelves…")["href"]
        return f"{self.GOODREADS_BASE_URL}{shelves_url}"

    @staticmethod
    @return_none_for_index_error
    def _get_unformatted_shelves(soup: bs4.BeautifulSoup) -> [str]:
        nodes = soup.find_all("div", {"class": "shelfStat"})
        return [" ".join(node.text.strip().split()) for node in nodes]

    @staticmethod
    def _get_shelf_name(shelf: str) -> str:
        return shelf.split()[:-2][0]

    @staticmethod
    def _get_shelf_count(shelf: str) -> int:
        return int(shelf.split()[-2].replace(",", ""))
