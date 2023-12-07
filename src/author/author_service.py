import functools
import re
import string
from functools import reduce
from typing import Dict, List, Optional

import dateutil
from dateutil import parser
from dateutil.relativedelta import relativedelta

# from src.common.errors.errors import return_none_for_attribute_error
# from src.common.utils.dict_operators import deep_get

def return_none_for_attribute_error(func):
    @functools.wraps(func)
    def wrapper(*args):
        """
        e.g Trying to get href from a non existent bs4 object.
        """
        try:
            return func(args[0])
        except AttributeError:
            return None

    return wrapper

def deep_get(dictionary, keys, default=None):
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split("."),
        dictionary,
    )


class AuthorService:
    def __init__(self, author_details_json: [Dict]):

        self.author_details_json = author_details_json

    # def _get_nested_result(self, key: str, first_result=True):
    #     results = list(
    #         set([deep_get(v, f"{key}.value") for v in self.author_details_json])
    #     )
    # 
    #     if first_result:
    #         return string.capwords(results[0])
    #     return [string.capwords(result) for result in results]

    # @return_none_for_attribute_error
    def get_birth_full_name(self) -> Optional[str]:
        """
        P1477
        Example: `Doris Lessing` was born `Doris May Tayler`
        Or in the case of `Octavio Paz Lozano` where `Lozano` is dropped
        """
        return deep_get(self.author_details_json, "birthFullName.value")

    @return_none_for_attribute_error
    def get_birth_full_name_in_native_language(self) -> Optional[str]:
        #  P1559
        return deep_get(
            self.author_details_json, "birthFullNameInNativeLanguageLabel.value"
        )

    @return_none_for_attribute_error
    def get_cause_of_death(self) -> Optional[str]:
        #  P509
        return deep_get(self.author_details_json, "causeOfDeathLabel.value").title()

    @return_none_for_attribute_error
    def get_country_of_citizenship(self) -> Optional[str]:
        #  P27
        result = deep_get(self.author_details_json, "countryOfCitizenshipLabel.value")
        if result:
            return result
        return ''

    @return_none_for_attribute_error
    def get_gender(self) -> Optional[str]:
        #  P21
        return deep_get(self.author_details_json, "genderLabel.value").title()

    @return_none_for_attribute_error
    def get_date_of_birth(self) -> Optional[str]:
        #  P569
        dob = deep_get(self.author_details_json, "dateOfBirthLabel.value")
        if dob:
            return dob.replace("T00:00:00Z", "")
        return None

    @return_none_for_attribute_error
    def get_place_of_birth(self) -> Optional[str]:
        #  P19
        return deep_get(self.author_details_json, "placeOfBirthLabel.value")

    @return_none_for_attribute_error
    def get_date_of_death(self) -> Optional[str]:
        #  P570
        dod = deep_get(self.author_details_json, "dateOfDeathLabel.value")
        if dod:
            return dod.replace("T00:00:00Z", "")
        return None

    @return_none_for_attribute_error
    def get_place_of_death(self) -> Optional[str]:
        #  P20
        return deep_get(self.author_details_json, "placeOfDeathLabel.value")

    @return_none_for_attribute_error
    def get_manner_of_death(self) -> Optional[str]:
        #  P1196
        return deep_get(self.author_details_json, "mannerOfDeathLabel.value").title()


    @staticmethod
    def _calculate_age_at_death(
        date_of_death: str, date_of_birth: str
    ) -> Optional[int]:

        if date_of_death:
            date_of_death_datetime_object = parser.parse(date_of_death).date()
            date_of_birth_datetime_object = parser.parse(date_of_birth).date()
            return relativedelta(
                date_of_death_datetime_object, date_of_birth_datetime_object
            ).years
        return None

    @return_none_for_attribute_error
    def get_age_at_death(self) -> Optional[str]:
        return deep_get(self.author_details_json, "ageAtDeathLabel.value")

    @return_none_for_attribute_error
    def get_place_of_burial(self) -> Optional[str]:
        #  P119
        return deep_get(self.author_details_json, "placeOfBurialLabel.value")

    @return_none_for_attribute_error
    def get_native_language(self) -> Optional[List[str]]:
        #  P103
        return deep_get(self.author_details_json, "writingLanguageLabel.value")

    @return_none_for_attribute_error
    def get_work_period_start_year(self) -> Optional[int]:
        #  P2031
        date = deep_get(self.author_details_json, "workPeriodStartLabel.value")
        if date:
            date_formatted = re.sub(
                r"-(?P<day>\d{2})-(?P<month>\d{2})(?P<time>t.+z)", "", date
            )

            return int(date_formatted.split("-")[0])
        return None

    @return_none_for_attribute_error
    def get_writing_languages(self) -> Optional[List[str]]:
        #  P6886
        return deep_get(
            self.author_details_json, "writingLanguageLabel.value"
        )

    @return_none_for_attribute_error
    def get_occupations(self) -> Optional[List[str]]:
        #  P106
        return deep_get(self.author_details_json, "occupationLabel.value").title()

    @return_none_for_attribute_error
    def get_literary_movements(self) -> Optional[List[str]]:
        #  P135
        return deep_get(
            self.author_details_json, "literaryMovementLabel.value"
        ).title()

    @return_none_for_attribute_error
    def get_educated_at(self) -> Optional[List[str]]:
        #  P69
        return deep_get(
            self.author_details_json, "educatedAtLabel.value"
        )

    @return_none_for_attribute_error
    def get_lifestyle(self) -> Optional[List[str]]:
        #  P1576
        return deep_get(
            self.author_details_json, "lifestyleLabel.value"
        ).title()

    @return_none_for_attribute_error
    def get_religion(self) -> Optional[str]:
        #  P140
        return deep_get(self.author_details_json, "religionLabel.value")

    @return_none_for_attribute_error
    def get_last_words(self) -> Optional[str]:
        #  P3909
        return deep_get(self.author_details_json, "lastWordsLabel.value")

    @return_none_for_attribute_error
    def get_notable_works(self) -> Optional[List[str]]:
        #  P800
        return deep_get(self.author_details_json, "notableWorksLabel.value")



    @return_none_for_attribute_error
    def get_genres(self) -> Optional[List[str]]:
        #  P136
        return deep_get(self.author_details_json, "genreLabel.value").title()


# author_json = {'item': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q278495'}, 'birthFullNameInNativeLanguage': {'xml:lang': 'en', 'type': 'literal', 'value': 'Marianne Moore'}, 'countryOfCitizenship': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q30'}, 'dateOfBirth': {'datatype': 'http://www.w3.org/2001/XMLSchema#dateTime', 'type': 'literal', 'value': '1887-11-15T00:00:00Z'}, 'dateOfDeath': {'datatype': 'http://www.w3.org/2001/XMLSchema#dateTime', 'type': 'literal', 'value': '1972-02-05T00:00:00Z'}, 'educatedAt': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q995265'}, 'gender': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q6581072'}, 'occupation': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q36180'}, 'placeOfBirth': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q963572'}, 'placeOfBurial': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q5417176'}, 'placeOfDeath': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q60'}, 'writingLanguage': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q1860'}, 'itemLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Marianne Moore'}, 'birthFullNameInNativeLanguageLabel': {'type': 'literal', 'value': 'Marianne Moore'}, 'countryOfCitizenshipLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'United States of America'}, 'dateOfBirthLabel': {'type': 'literal', 'value': '1887-11-15T00:00:00Z'}, 'dateOfDeathLabel': {'type': 'literal', 'value': '1972-02-05T00:00:00Z'}, 'educatedAtLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Bryn Mawr College'}, 'genderLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'female'}, 'occupationLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'writer'}, 'placeOfBirthLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Kirkwood'}, 'placeOfBurialLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Evergreen Cemetery'}, 'placeOfDeathLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'New York City'}, 'writingLanguageLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'English'}}
#
#
# author_service = AuthorService(author_json)
# #
# print(author_service.get_gender())
