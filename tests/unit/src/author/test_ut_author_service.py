from data.jane_austen import jane_austen_sparql_response

from src.author.author_service import AuthorService


class TestAuthorServiceParser:
    def setup_method(self):
        self.author_service = AuthorService(jane_austen_sparql_response)

    def test_get_gender(self):
        assert self.author_service.get_gender() == "Female"

    def test_get_country_of_citizenship(self):
        assert self.author_service.get_country_of_citizenship() == "Kingdom of Great Britain"

    def test_get_birth_full_name_in_native_language(self):
        assert self.author_service.get_birth_full_name_in_native_language() == "Jane Austen"

    def test_get_birth_full_name(self):
        assert self.author_service.get_birth_full_name() == "Jane Austen"

    def test_get_date_of_birth(self):
        assert self.author_service.get_date_of_birth() == "1775-12-16"

    def test_get_place_of_birth(self):
        assert self.author_service.get_place_of_birth() == "Steventon"

    def test_get_date_of_death(self):
        assert self.author_service.get_date_of_death() == "1817-07-18"

    def test_get_place_of_death(self):
        assert self.author_service.get_place_of_death() == "Winchester"

    def test_manner_of_death(self):
        assert self.author_service.get_manner_of_death() == "Natural Causes"

    def test_get_cause_of_death(self):
        assert self.author_service.get_cause_of_death() == "Addison's disease"

    def test_calculate_age_at_death(self):
        date_of_death = "2013-11-17"
        date_of_birth = "1919-10-22"
        assert self.author_service._calculate_age_at_death(date_of_death, date_of_birth) == 94

    def test_get_age_at_death(self):
        assert self.author_service.get_age_at_death() is None

    def test_get_place_of_burial(self):
        assert self.author_service.get_place_of_burial() == "Winchester Cathedral"

    def test_get_native_language(self):
        assert self.author_service.get_native_language() == "English"

    def test_get_writing_language(self):
        assert self.author_service.get_writing_languages() == "English"

    def test_get_occupation(self):
        expected = "Writer"
        assert self.author_service.get_occupation() == expected

    def test_get_literary_movement(self):
        assert self.author_service.get_literary_movements() == "Literary Realism"

    def test_get_educated_at(self):
        assert self.author_service.get_educated_at() == "Bournemouth University"

    def test_get_lifestyle(self):
        assert self.author_service.get_lifestyle() is None

    def test_get_religion(self):
        assert self.author_service.get_religion() == "Anglicanism"

    def test_get_last_words(self):
        assert self.author_service.get_last_words() is None

    def test_get_get_notable_work(self):
        expected = "Persuasion"
        assert self.author_service.get_notable_work() == expected

    def test_get_genres(self):
        assert self.author_service.get_genre() == "Romance Novel"

    def test_get_work_period_start_year(self):
        assert self.author_service.get_work_period_start_year() == "1787"
