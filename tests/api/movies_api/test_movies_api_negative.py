import allure
import pytest
from utils.data_generator import DataGenerator


class TestMoviesApiNegative:

    @allure.title("Создание фильма без обязательных полей")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("API фильмов")
    @allure.story("Негативные тесты")
    @pytest.mark.negative
    @pytest.mark.critical
    def test_create_movie_missing_fields(self, authenticated_admin):
        invalid_fields = {"name": "test"}

        with allure.step("Отправка запроса с неполными данными"):
            authenticated_admin.movies_api.create_movie(invalid_fields, expected_status=400)

    @allure.title("Создание фильма с отрицательной ценой")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("API фильмов")
    @allure.story("Негативные тесты")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_create_movie_with_negative_price(self, authenticated_admin, valid_genre_id):
        movie_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)
        movie_data["price"] = -100

        with allure.step("Отправка запроса с отрицательной ценой"):
            response = authenticated_admin.movies_api.create_movie(movie_data, expected_status=400)
            error_data = response.json()

        with allure.step("Проверка сообщения об ошибке"):
            assert "Поле price должно быть больше 0" in error_data["message"]

    @allure.title("Создание фильма с невалидной локацией")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("API фильмов")
    @allure.story("Негативные тесты")
    @pytest.mark.negative
    def test_create_movie_with_invalid_loc(self, authenticated_admin, valid_genre_id):
        movie_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)
        movie_data["location"] = "INVALID/CITY"

        with allure.step("Отправка запроса с невалидной локацией"):
            authenticated_admin.movies_api.create_movie(movie_data, expected_status=400)

    @allure.title("Получение несуществующего фильма")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("API фильмов")
    @allure.story("Негативные тесты")
    @pytest.mark.negative
    @pytest.mark.smoke
    def test_get_movie_by_noname_id(self, authenticated_admin):
        with allure.step("Отправка запроса с несуществующим ID"):
            authenticated_admin.movies_api.get_movie_by_id(12312321, expected_status=404)

    @allure.title("Обновление несуществующего фильма")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("API фильмов")
    @allure.story("Негативные тесты")
    @pytest.mark.negative
    def test_update_noname_movie(self, authenticated_admin):
        update_data = {"name": "Updated Name"}

        with allure.step("Отправка запроса на обновление несуществующего фильма"):
            authenticated_admin.movies_api.update_movie(132123123, update_data, expected_status=404)

    @allure.title("Удаление несуществующего фильма")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("API фильмов")
    @allure.story("Негативные тесты")
    @pytest.mark.negative
    def test_delete_noname_movie(self, authenticated_admin):
        with allure.step("Отправка запроса на удаление несуществующего фильма"):
            authenticated_admin.movies_api.delete_movie(12312312, expected_status=404)

    @allure.title("Создание фильма с пустым названием")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("API фильмов")
    @allure.story("Негативные тесты")
    @pytest.mark.negative
    @pytest.mark.regression
    def test_create_movie_with_empty_name(self, authenticated_admin, valid_genre_id):
        movie_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)
        movie_data["name"] = ""

        with allure.step("Отправка запроса с пустым названием"):
            authenticated_admin.movies_api.create_movie(movie_data, expected_status=400)