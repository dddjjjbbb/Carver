import re
import string
from typing import Dict, List, Optional

from dateutil import parser
<<<<<<< HEAD
=======
from dateutil.parser._parser import ParserError
>>>>>>> b2ba7b2 (migrate to new machine)
from dateutil.relativedelta import relativedelta

from src.common.errors.errors import return_none_for_attribute_error
from src.common.utils.dict_operators import deep_get
<<<<<<< HEAD


class AuthorService:
    def __init__(self, author_details_json: [Dict]):

        self.author_details_json = author_details_json
=======
from src.author.sparql_queries import sparql_search_query
import sys

class AuthorSearchService:
    def __init__(self, author_name: str):

        self.author_name = author_name

    def insert_into_sparql_query(self) -> str:
        return sparql_search_query.replace("QUERY", self.author_name)

    def get_results(self) -> Dict:
        ENDPOINT_URL = "https://query.wikidata.org/sparql"

        vi1, vi2 = (
            sys.version_info[0],
            sys.version_info[1],
        )
        user_agent = f"WDQS-example Python/{vi1}.{vi2}"

        # TODO adjust user agent; see https://w.wiki/CX6
        sparql = SPARQLWrapper(ENDPOINT_URL, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()




class AuthorParseService:
    def __init__(self, author_details: [Dict]):

        self.author_details_json = author_details
>>>>>>> b2ba7b2 (migrate to new machine)

    def _get_nested_result(self, key: str, first_result=True):
        results = list(
            set([deep_get(v, f"{key}.value") for v in self.author_details_json])
        )
        if first_result:
            return string.capwords(results[0])
        return [string.capwords(result) for result in results]

<<<<<<< HEAD
=======

>>>>>>> b2ba7b2 (migrate to new machine)
    @return_none_for_attribute_error
    def get_birth_full_name(self) -> Optional[str]:
        """
        P1477
        Example: `Doris Lessing` was born `Doris May Tayler`
        Or in the case of `Octavio Paz Lozano` where `Lozano` is dropped
        """
<<<<<<< HEAD
        return AuthorService._get_nested_result(self, "birthFullName")
=======
        return AuthorParseService._get_nested_result(self, "birthFullName")
>>>>>>> b2ba7b2 (migrate to new machine)

    @return_none_for_attribute_error
    def get_birth_full_name_in_native_language(self) -> Optional[str]:
        #  P1559
<<<<<<< HEAD
        return AuthorService._get_nested_result(
=======
        return AuthorParseService._get_nested_result(
>>>>>>> b2ba7b2 (migrate to new machine)
            self, "birthFullNameInNativeLanguageLabel"
        )

    @return_none_for_attribute_error
    def get_cause_of_death(self) -> Optional[str]:
        #  P509
<<<<<<< HEAD
        return AuthorService._get_nested_result(self, "causeOfDeathLabel")
=======
        return AuthorParseService._get_nested_result(self, "causeOfDeathLabel")
>>>>>>> b2ba7b2 (migrate to new machine)

    @return_none_for_attribute_error
    def get_country_of_citizenship(self) -> Optional[str]:
        #  P27
<<<<<<< HEAD
        return AuthorService._get_nested_result(self, "countryOfCitizenshipLabel")
=======
        return AuthorParseService._get_nested_result(self, "countryOfCitizenshipLabel")
>>>>>>> b2ba7b2 (migrate to new machine)

    @return_none_for_attribute_error
    def get_gender(self) -> Optional[str]:
        #  P21
<<<<<<< HEAD
        return AuthorService._get_nested_result(self, "genderLabel")
=======
        return AuthorParseService._get_nested_result(self, "genderLabel")
>>>>>>> b2ba7b2 (migrate to new machine)

    @return_none_for_attribute_error
    def get_date_of_birth(self) -> Optional[str]:
        #  P569
<<<<<<< HEAD
        dob = AuthorService._get_nested_result(self, "dateOfBirthLabel")
=======
        dob = AuthorParseService._get_nested_result(self, "dateOfBirthLabel")
>>>>>>> b2ba7b2 (migrate to new machine)
        if dob:
            return dob.replace("t00:00:00z", "")
        return None

    @return_none_for_attribute_error
    def get_place_of_birth(self) -> Optional[str]:
        #  P19
<<<<<<< HEAD
        return AuthorService._get_nested_result(self, "placeOfBirthLabel")
=======
        return AuthorParseService._get_nested_result(self, "placeOfBirthLabel")
>>>>>>> b2ba7b2 (migrate to new machine)

    @return_none_for_attribute_error
    def get_date_of_death(self) -> Optional[str]:
        #  P570
<<<<<<< HEAD
        dod = AuthorService._get_nested_result(self, "dateOfDeathLabel")
=======
        dod = AuthorParseService._get_nested_result(self, "dateOfDeathLabel")
>>>>>>> b2ba7b2 (migrate to new machine)
        if dod:
            return dod.replace("t00:00:00z", "")
        return None

    @return_none_for_attribute_error
    def get_place_of_death(self) -> Optional[str]:
        #  P20
<<<<<<< HEAD
        return AuthorService._get_nested_result(self, "placeOfDeathLabel")
=======
        return AuthorParseService._get_nested_result(self, "placeOfDeathLabel")
>>>>>>> b2ba7b2 (migrate to new machine)

    @return_none_for_attribute_error
    def get_manner_of_death(self) -> Optional[str]:
        #  P1196
<<<<<<< HEAD
        return AuthorService._get_nested_result(self, "mannerOfDeathLabel")
=======
        return AuthorParseService._get_nested_result(self, "mannerOfDeathLabel")
>>>>>>> b2ba7b2 (migrate to new machine)

    @staticmethod
    def _calculate_age_at_death(
        date_of_death: str, date_of_birth: str
    ) -> Optional[int]:
<<<<<<< HEAD

        if date_of_death:
            date_of_death_datetime_object = parser.parse(date_of_death).date()
            date_of_birth_datetime_object = parser.parse(date_of_birth).date()
            return relativedelta(
                date_of_death_datetime_object, date_of_birth_datetime_object
            ).years
        return None

    @return_none_for_attribute_error
    def get_age_at_death(self) -> Optional[str]:
        return AuthorService._get_nested_result(self, "ageAtDeathLabel")
=======
        try:

            if date_of_death:
                date_of_death_datetime_object = parser.parse(date_of_death).date()
                date_of_birth_datetime_object = parser.parse(date_of_birth).date()
                return relativedelta(
                    date_of_death_datetime_object, date_of_birth_datetime_object
                ).years
            return None
        except ParserError:
            return None

    @return_none_for_attribute_error
    def get_age_at_death(self) -> Optional[str]:
        return AuthorParseService._get_nested_result(self, "ageAtDeathLabel")
>>>>>>> b2ba7b2 (migrate to new machine)

    @return_none_for_attribute_error
    def get_place_of_burial(self) -> Optional[str]:
        #  P119
<<<<<<< HEAD
        return AuthorService._get_nested_result(self, "placeOfBurialLabel")
=======
        return AuthorParseService._get_nested_result(self, "placeOfBurialLabel")
>>>>>>> b2ba7b2 (migrate to new machine)

    @return_none_for_attribute_error
    def get_native_language(self) -> Optional[List[str]]:
        #  P103
<<<<<<< HEAD
        return AuthorService._get_nested_result(self, "writingLanguageLabel")
=======
        return AuthorParseService._get_nested_result(self, "writingLanguageLabel")
>>>>>>> b2ba7b2 (migrate to new machine)

    @return_none_for_attribute_error
    def get_work_period_start_year(self) -> Optional[int]:
        #  P2031
<<<<<<< HEAD
        date = AuthorService._get_nested_result(self, "workPeriodStartLabel")
=======
        date = AuthorParseService._get_nested_result(self, "workPeriodStartLabel")
>>>>>>> b2ba7b2 (migrate to new machine)
        if date:
            date_formatted = re.sub(
                r"-(?P<day>\d{2})-(?P<month>\d{2})(?P<time>t.+z)", "", date
            )
            return int(date_formatted)
        return None

    @return_none_for_attribute_error
    def get_writing_languages(self) -> Optional[List[str]]:
        #  P6886
<<<<<<< HEAD
        return AuthorService._get_nested_result(
=======
        return AuthorParseService._get_nested_result(
>>>>>>> b2ba7b2 (migrate to new machine)
            self, "writingLanguageLabel", first_result=False
        )

    @return_none_for_attribute_error
    def get_occupations(self) -> Optional[List[str]]:
        #  P106
        return sorted(
<<<<<<< HEAD
            AuthorService._get_nested_result(
=======
            AuthorParseService._get_nested_result(
>>>>>>> b2ba7b2 (migrate to new machine)
                self, "occupationLabel", first_result=False
            )
        )

    @return_none_for_attribute_error
    def get_literary_movements(self) -> Optional[List[str]]:
        #  P135
<<<<<<< HEAD
        return AuthorService._get_nested_result(
=======
        return AuthorParseService._get_nested_result(
>>>>>>> b2ba7b2 (migrate to new machine)
            self, "literaryMovementLabel", first_result=False
        )

    @return_none_for_attribute_error
    def get_educated_at(self) -> Optional[List[str]]:
        #  P69
<<<<<<< HEAD
        return AuthorService._get_nested_result(
=======
        return AuthorParseService._get_nested_result(
>>>>>>> b2ba7b2 (migrate to new machine)
            self, "educatedAtLabel", first_result=False
        )

    @return_none_for_attribute_error
    def get_lifestyle(self) -> Optional[List[str]]:
        #  P1576
<<<<<<< HEAD
        return AuthorService._get_nested_result(
=======
        return AuthorParseService._get_nested_result(
>>>>>>> b2ba7b2 (migrate to new machine)
            self, "lifestyleLabel", first_result=False
        )

    @return_none_for_attribute_error
    def get_religion(self) -> Optional[str]:
        #  P140
<<<<<<< HEAD
        return AuthorService._get_nested_result(self, "religionLabel")
=======
        return AuthorParseService._get_nested_result(self, "religionLabel")
>>>>>>> b2ba7b2 (migrate to new machine)

    @return_none_for_attribute_error
    def get_last_words(self) -> Optional[str]:
        #  P3909
<<<<<<< HEAD
        return AuthorService._get_nested_result(self, "lastWordsLabel")
=======
        return AuthorParseService._get_nested_result(self, "lastWordsLabel")
>>>>>>> b2ba7b2 (migrate to new machine)

    @return_none_for_attribute_error
    def get_notable_works(self) -> Optional[List[str]]:
        #  P800
        return sorted(
<<<<<<< HEAD
            AuthorService._get_nested_result(
=======
            AuthorParseService._get_nested_result(
>>>>>>> b2ba7b2 (migrate to new machine)
                self, "notableWorksLabel", first_result=False
            )
        )

    @return_none_for_attribute_error
    def get_genres(self) -> Optional[List[str]]:
        #  P136
<<<<<<< HEAD
        return AuthorService._get_nested_result(self, "genreLabel", first_result=False)
=======
        return AuthorParseService._get_nested_result(self, "genreLabel", first_result=False)
>>>>>>> b2ba7b2 (migrate to new machine)
