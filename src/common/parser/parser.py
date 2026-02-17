import bs4
from requests import Response


def parse(response: Response) -> bs4.BeautifulSoup:
    return bs4.BeautifulSoup(response.text, "html.parser")
