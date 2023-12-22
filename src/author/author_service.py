from functools import reduce
from typing import Dict, List, Optional

from dateutil import parser
from dateutil.relativedelta import relativedelta

from src.common.errors.errors import return_none_for_attribute_error


def deep_get(dictionary, keys, default=None):
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split("."),
        dictionary,
    )


class AuthorService:
    def __init__(self, author_details_json: [Dict]):
        self.author_details_json = author_details_json
        print(self.author_details_json)

    def get_birth_full_name(self) -> Optional[str]:
        """
        P1477
        Example: `Doris Lessing` was born `Doris May Tayler`
        Or in the case of `Octavio Paz Lozano` where `Lozano` is dropped
        """
        result = deep_get(self.author_details_json, "birthFullName.value")
        if result:
            return "".join(result).title()
        return ""

    @return_none_for_attribute_error
    def get_birth_full_name_in_native_language(self) -> Optional[str]:
        #  P1559
        result = deep_get(
            self.author_details_json, "birthFullNameInNativeLanguageLabel.value"
        )
        if result:
            return "".join(result).title()
        return ""

    @return_none_for_attribute_error
    def get_cause_of_death(self) -> Optional[str]:
        #  P509
        result = deep_get(self.author_details_json, "causeOfDeathLabel.value")
        if result:
            return "".join(result)
        return ""

    @return_none_for_attribute_error
    def get_country_of_citizenship(self) -> Optional[str]:
        #  P27
        result = deep_get(self.author_details_json, "countryOfCitizenshipLabel.value")
        if result:
            return "".join(result)

        return None

    @return_none_for_attribute_error
    def get_gender(self) -> Optional[str]:
        #  P21
        result = deep_get(self.author_details_json, "genderLabel.value")
        if result:
            return "".join(result).title()
        return None

    @return_none_for_attribute_error
    def get_date_of_birth(self) -> Optional[str]:
        #  P569
        dob = deep_get(self.author_details_json, "dateOfBirthLabel.value")
        if dob:
            return dob.replace("T00:00:00Z", "")

        return ""

    @return_none_for_attribute_error
    def get_place_of_birth(self) -> Optional[str]:
        #  P19
        result = deep_get(self.author_details_json, "placeOfBirthLabel.value")
        if result:
            return "".join(result).title()
        return ""

    @return_none_for_attribute_error
    def get_date_of_death(self) -> Optional[str]:
        #  P570
        dod = deep_get(self.author_details_json, "dateOfDeathLabel.value")
        if dod:
            return dod.replace("T00:00:00Z", "")
        return ""

    @return_none_for_attribute_error
    def get_place_of_death(self) -> Optional[str]:
        #  P20
        result = deep_get(self.author_details_json, "placeOfDeathLabel.value")

        if result:
            return "".join(result).title()
        return ""

    @return_none_for_attribute_error
    def get_manner_of_death(self) -> Optional[str]:
        #  P1196
        result = deep_get(self.author_details_json, "mannerOfDeathLabel.value")
        if result:
            return "".join(result).title()
        return ""

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
        # example: 1787-01-01T00:00:00Z
        date = deep_get(self.author_details_json, "workPeriodStartLabel.value")
        if date:
            return date.split("-")[0]
        return None

    @return_none_for_attribute_error
    def get_writing_languages(self) -> Optional[List[str]]:
        #  P6886
        return deep_get(self.author_details_json, "writingLanguageLabel.value")

    @return_none_for_attribute_error
    def get_occupation(self) -> Optional[str]:
        #  P106
        result = deep_get(self.author_details_json, "occupationLabel.value")
        if result:
            return "".join(result).title()
        return None

    @return_none_for_attribute_error
    def get_literary_movements(self) -> Optional[str]:
        #  P135
        result = deep_get(self.author_details_json, "literaryMovementLabel.value")
        if result:
            return "".join(result).title()
        return None

    @return_none_for_attribute_error
    def get_educated_at(self) -> Optional[str]:
        #  P69
        return deep_get(self.author_details_json, "educatedAtLabel.value")

    @return_none_for_attribute_error
    def get_lifestyle(self) -> Optional[str]:
        #  P1576
        return deep_get(self.author_details_json, "lifestyleLabel.value")

    @return_none_for_attribute_error
    def get_religion(self) -> Optional[str]:
        #  P140
        return deep_get(self.author_details_json, "religionLabel.value")

    @return_none_for_attribute_error
    def get_last_words(self) -> Optional[str]:
        #  P3909
        result = deep_get(self.author_details_json, "lastWordsLabel.value")

    @return_none_for_attribute_error
    def get_notable_work(self) -> Optional[str]:
        #  P800
        result = deep_get(self.author_details_json, "notableWorksLabel.value")
        if result:
            return "".join(result).title()
        return None

    @return_none_for_attribute_error
    def get_genre(self) -> Optional[str]:
        #  P136
        result = deep_get(self.author_details_json, "genreLabel.value")
        if result:
            return "".join(result).title()
        return None
