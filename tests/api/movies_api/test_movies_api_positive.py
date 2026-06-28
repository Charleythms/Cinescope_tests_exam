import allure
import pytest

from models.base_models import MovieResponse, MoviesListResponse
from utils.data_generator import DataGenerator


class TestMoviesApiPositive:

    @allure.title("Получение списка фильмов")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("API фильмов")
    @allure.story("Получение фильмов")
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_movies(self, authenticated_admin):
        with allure.step("Запрос списка фильмов"):
            response = authenticated_admin.movies_api.get_movies(expected_status=200)

        with allure.step("Валидация структуры ответа"):
            MoviesListResponse(**response.json())

    @allure.title("Создание нового фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("API фильмов")
    @allure.story("Создание фильма")
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_create_movie(self, authenticated_admin, valid_genre_id):
        movie_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)

        with allure.step("Создание фильма через API"):
            response = authenticated_admin.movies_api.create_movie(movie_data)
            created_movie = MovieResponse(**response.json())

        with allure.step("Проверка данных созданного фильма"):
            assert created_movie.name == movie_data["name"], "Название не совпадает"
            assert created_movie.description == movie_data["description"], "Описание не совпадает"
            assert created_movie.price == movie_data["price"], "Цена не совпадает"
            assert created_movie.location == movie_data["location"], "Локация не совпадает"
            assert created_movie.published == movie_data["published"], "Статус публикации не совпадает"
            assert created_movie.genreId == movie_data["genreId"], "ID жанра не совпадает"

        with allure.step("Удаление созданного фильма"):
            authenticated_admin.movies_api.delete_movie(created_movie.id)
            authenticated_admin.movies_api.get_movie_by_id(created_movie.id, expected_status=404)

    @allure.title("Получение фильма по идентификатору")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("API фильмов")
    @allure.story("Получение фильма по ID")
    @pytest.mark.regression
    def test_get_movie_by_id(self, authenticated_admin, valid_genre_id):
        movie_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)

        with allure.step("Создание фильма"):
            create_response = authenticated_admin.movies_api.create_movie(movie_data, expected_status=201)
            created_movie = MovieResponse(**create_response.json())
            movie_id = created_movie.id

        with allure.step("Получение фильма по ID"):
            response = authenticated_admin.movies_api.get_movie_by_id(movie_id, expected_status=200)
            fetched_movie = MovieResponse(**response.json())

        with allure.step("Проверка данных полученного фильма"):
            assert fetched_movie.id == movie_id, "ID не совпадает"
            assert fetched_movie.name == movie_data["name"], "Название не совпадает"
            assert fetched_movie.description == movie_data["description"], "Описание не совпадает"
            assert fetched_movie.price == movie_data["price"], "Цена не совпадает"
            assert fetched_movie.location == movie_data["location"], "Локация не совпадает"
            assert fetched_movie.published == movie_data["published"], "Статус публикации не совпадает"
            assert fetched_movie.genreId == movie_data["genreId"], "ID жанра не совпадает"

        with allure.step("Удаление фильма"):
            authenticated_admin.movies_api.delete_movie(movie_id)
            authenticated_admin.movies_api.get_movie_by_id(movie_id, expected_status=404)

    @allure.title("Обновление существующего фильма")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("API фильмов")
    @allure.story("Обновление фильма")
    @pytest.mark.regression
    def test_update_movie(self, authenticated_admin, valid_genre_id):
        movie_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)

        with allure.step("Создание фильма"):
            create_response = authenticated_admin.movies_api.create_movie(movie_data, expected_status=201)
            created_movie = MovieResponse(**create_response.json())
            movie_id = created_movie.id

        try:
            updated_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)

            with allure.step("Обновление фильма"):
                response = authenticated_admin.movies_api.update_movie(movie_id, updated_data, expected_status=200)
                updated_movie = MovieResponse(**response.json())

            with allure.step("Проверка обновленных данных"):
                assert updated_movie.id == movie_id, "ID не совпадает"
                assert updated_movie.name == updated_data["name"], "Название не обновилось"
                assert updated_movie.description == updated_data["description"], "Описание не обновилось"
                assert updated_movie.price == updated_data["price"], "Цена не обновилась"
                assert updated_movie.location == updated_data["location"], "Локация не обновилась"
                assert updated_movie.published == updated_data["published"], "Статус публикации не обновился"
                assert updated_movie.genreId == updated_data["genreId"], "ID жанра не обновился"

        finally:
            with allure.step("Удаление фильма"):
                authenticated_admin.movies_api.delete_movie(movie_id)
                authenticated_admin.movies_api.get_movie_by_id(movie_id, expected_status=404)

    @allure.title("Удаление существующего фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("API фильмов")
    @allure.story("Удаление фильма")
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_delete_movie(self, authenticated_admin, valid_genre_id):
        movie_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)

        with allure.step("Создание фильма"):
            create_response = authenticated_admin.movies_api.create_movie(movie_data, expected_status=201)
            created_movie = MovieResponse(**create_response.json())
            movie_id = created_movie.id

        with allure.step("Удаление фильма"):
            authenticated_admin.movies_api.delete_movie(movie_id)

        with allure.step("Проверка что фильм удален"):
            authenticated_admin.movies_api.get_movie_by_id(movie_id, expected_status=404)