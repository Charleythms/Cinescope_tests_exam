import allure
import pytest
from models.base_models import MovieResponse
from utils.data_generator import DataGenerator


class TestMoviesApiParameterized:

    @allure.title("Фильтрация фильмов по локациям")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("API фильмов")
    @allure.story("Фильтрация фильмов")
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.parametrize("location", [
        "MSK",
        "SPB"
    ])
    def test_filter_movies_by_location(self, authenticated_admin, location):
        with allure.step(f"Запрос фильмов с фильтром по локации {location}"):
            response = authenticated_admin.movies_api.get_movies(
                params={"locations": location, "pageSize": 20},
                expected_status=200
            )
            data = response.json()

        with allure.step(f"Проверка что все фильмы имеют локацию {location}"):
            for movie_data in data['movies']:
                movie = MovieResponse(**movie_data)

    @allure.title("Создание фильма с разным статусом публикации")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("API фильмов")
    @allure.story("Параметризованные тесты")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("published", [
        True,
        False
    ])
    def test_create_movie_with_different_publish_status(self, super_admin, valid_genre_id, published):
        movie_data = DataGenerator.generate_movie_data(
            genre_id=valid_genre_id,
            published=published
        )

        with allure.step(f"Создание фильма со статусом публикации {published}"):
            create_response = super_admin.api.movies_api.create_movie(movie_data, expected_status=201)
            created_movie = MovieResponse(**create_response.json())
            movie_id = created_movie.id

        try:
            with allure.step("Проверка данных созданного фильма"):
                assert created_movie.published == published, f"Статус публикации должен быть {published}"
                assert created_movie.name == movie_data["name"], "Название не совпадает"
                assert created_movie.price == movie_data["price"], "Цена не совпадает"

        finally:
            with allure.step("Удаление фильма"):
                super_admin.api.movies_api.delete_movie(movie_id, expected_status=200)