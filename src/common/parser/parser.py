from typing import Union

import bs4

from src.common.errors.errors import return_none_for_type_error
from requests import Response


# @return_none_for_type_error
def parse(response: Response) -> bs4.BeautifulSoup:
    return bs4.BeautifulSoup(response.text, "html.parser")

