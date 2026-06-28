import allure
import pytest
from models.base_models import MovieResponse


class TestMoviesApiFilters:

    @allure.title("Фильтрация фильмов по локации")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("API фильмов")
    @allure.story("Фильтрация фильмов")
    @pytest.mark.smoke
    @pytest.mark.filters
    def test_filter_by_location(self, authenticated_admin):
        with allure.step("Запрос фильмов с фильтром по локации SPB"):
            response = authenticated_admin.movies_api.get_movies(
                params={"locations": "SPB", "pageSize": 20},
                expected_status=200
            )
            data = response.json()

        with allure.step("Проверка что все фильмы имеют локацию SPB"):
            for movie_data in data.get("movies", []):
                movie = MovieResponse(**movie_data)
                assert movie.location == "SPB", f"Локация {movie.location} не соответствует SPB"

    @allure.title("Фильтрация фильмов по жанру")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("API фильмов")
    @allure.story("Фильтрация фильмов")
    @pytest.mark.smoke
    @pytest.mark.filters
    def test_filter_by_genre(self, authenticated_admin):
        target_genre_id = 3

        with allure.step(f"Запрос фильмов с фильтром по жанру {target_genre_id}"):
            response = authenticated_admin.movies_api.get_movies(
                params={"genreId": target_genre_id, "pageSize": 20},
                expected_status=200
            )
            data = response.json()

        with allure.step(f"Проверка что все фильмы имеют жанр {target_genre_id}"):
            for movie_data in data.get("movies", []):
                movie = MovieResponse(**movie_data)
                assert movie.genreId == target_genre_id, f"ID жанра {movie.genreId} не соответствует {target_genre_id}"