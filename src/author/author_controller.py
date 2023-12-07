# TODO offer config option to infer `writingLanguages` from `countryOfCitizenship` if known
# TODO check encoding issues such as `Patrick Suskind`
# TODO check strange results for `Mikhail Lermontov`

import sys
from pprint import pprint


from .author_config import config_age_at_death
from .author_config import config_birth_full_name
from .author_config import config_birth_full_name_in_native_language
from .author_config import config_cause_of_death
from .author_config import config_country_of_citizenship
from .author_config import config_date_of_birth
from .author_config import config_date_of_death
from .author_config import config_educated_at
from .author_config import config_gender
from .author_config import config_genres
from .author_config import config_last_words
from .author_config import config_lifestyle
from .author_config import config_literary_movements
from .author_config import config_manner_of_death
from .author_config import config_native_language
from .author_config import config_notable_works
from .author_config import config_occupations
from .author_config import config_place_of_birth
from .author_config import config_place_of_burial
from .author_config import config_place_of_death
from .author_config import config_religion
from .author_config import config_work_period_start_year
from .author_config import config_writing_languages

sys.path.append(r"/Users/daniel/PycharmProjects/carver")

from src.author.author_service import AuthorService


from typing import Dict

from SPARQLWrapper import JSON
from SPARQLWrapper import SPARQLWrapper

from .author_model import AuthorModel
from .sparql_queries import author_details_query
from .sparql_queries import search_query
from src.common.utils.dict_operators import deep_get

ENDPOINT_URL = "https://query.wikidata.org/sparql"

vi1, vi2 = (
    sys.version_info[0],
    sys.version_info[1],
)

USER_AGENT = f"WDQS-example Python/{vi1}.{vi2}"


def insert_into_sparql_query(query: str) -> str:
    return search_query.replace("QUERY", query)


def get_results(query: str) -> [Dict]:
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(ENDPOINT_URL, agent=USER_AGENT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


# @return_none_for_index_error
def build_author_model(author_name: str) -> AuthorModel:

    query = search_query.replace("QUERY", author_name)

    # Note: This can return an empty list
    try:
        results = get_results(query)["results"]["bindings"][0]

        code = deep_get(results, "item.value").rsplit("/", 1)[-1]

        author_query = author_details_query.replace("QUERY", code)

        author_details = get_results(author_query)

        author_details_json = author_details["results"]["bindings"][0]

        author_service = AuthorService(author_details_json)

        author_model = AuthorModel(
            age_at_death=author_service._calculate_age_at_death(
                author_service.get_date_of_death(), author_service.get_date_of_birth()
            )
            if config_age_at_death is True
            else None,
            birth_full_name=author_service.get_birth_full_name()
            if config_birth_full_name is True
            else None,
            birth_full_name_in_native_language=author_service.get_birth_full_name_in_native_language()
            if config_birth_full_name_in_native_language is True
            else None,
            cause_of_death=author_service.get_cause_of_death()
            if config_cause_of_death is True
            else None,
            country_of_citizenship=author_service.get_country_of_citizenship()
            if config_country_of_citizenship is True
            else None,
            date_of_birth=author_service.get_date_of_birth()
            if config_date_of_birth is True
            else None,
            date_of_death=author_service.get_date_of_death()
            if config_date_of_death is True
            else None,
            educated_at=author_service.get_educated_at()
            if config_educated_at is True
            else None,
            gender=author_service.get_gender() if config_gender is True else None,
            genres=author_service.get_genres() if config_genres is True else None,
            lifestyle=author_service.get_lifestyle() if config_lifestyle is True else None,
            literary_movements=author_service.get_literary_movements()
            if config_literary_movements is True
            else None,
            manner_of_death=author_service.get_manner_of_death()
            if config_manner_of_death is True
            else None,
            native_language=author_service.get_native_language()
            if config_native_language is True
            else None,
            notable_works=author_service.get_notable_works()
            if config_notable_works is True
            else None,
            occupations=author_service.get_occupations()
            if config_occupations is True
            else None,
            place_of_birth=author_service.get_place_of_birth()
            if config_place_of_birth is True
            else None,
            place_of_burial=author_service.get_place_of_burial()
            if config_place_of_burial is True
            else None,
            place_of_death=author_service.get_place_of_death()
            if config_place_of_death is True
            else None,
            religion=author_service.get_religion() if config_religion is True else None,
            last_words=author_service.get_last_words()
            if config_last_words is True
            else None,
            work_period_start_year=author_service.get_work_period_start_year()
            if config_work_period_start_year is True
            else None,
            writing_languages=author_service.get_writing_languages()
            if config_writing_languages is True
            else None,
        )

        return author_model
    except IndexError:
        return ''


def split_wikidata_uri_value_on_identifier(wikidata_uri_value) -> str:
    return wikidata_uri_value.rsplit("/", 1)[-1]


def get_wikidata_code_for_author(sparql_result: Dict) -> str:
    wikidata_uri_value = deep_get(sparql_result, "item.value")
    return split_wikidata_uri_value_on_identifier(wikidata_uri_value)


def generate_author_details(wikidata_code_for_author: str) -> Dict:
    author_query = insert_into_sparql_query(wikidata_code_for_author)
    author_details = get_results(author_query)
    return author_details
