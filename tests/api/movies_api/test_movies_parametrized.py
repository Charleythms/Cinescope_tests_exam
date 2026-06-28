import allure
import pytest
from models.base_models import MovieResponse
from utils.data_generator import DataGenerator


class TestMoviesApiParameterized:

    @allure.title("Создание фильма с разными ценами")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("API фильмов")
    @allure.story("Параметризованные тесты")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("price", [
        100,
        1000,
        5000,
        9999
    ])
    def test_create_movie_with_different_prices(self, super_admin, valid_genre_id, price):
        movie_data = DataGenerator.generate_movie_data(
            genre_id=valid_genre_id,
            price=price
        )

        with allure.step(f"Создание фильма с ценой {price}"):
            create_response = super_admin.api.movies_api.create_movie(movie_data, expected_status=201)
            created_movie = MovieResponse(**create_response.json())
            movie_id = created_movie.id
            allure.attach(
                f"ID созданного фильма: {movie_id}",
                name="ID фильма",
                attachment_type=allure.attachment_type.TEXT
            )

        try:
            with allure.step("Проверка данных созданного фильма"):
                assert created_movie.price == price, f"Цена должна быть {price}"
                assert created_movie.name == movie_data["name"], "Название не совпадает"
                assert created_movie.location == movie_data["location"], "Локация не совпадает"

        finally:
            with allure.step("Удаление фильма"):
                super_admin.api.movies_api.delete_movie(movie_id, expected_status=200)

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