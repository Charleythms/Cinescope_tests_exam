import allure
import pytest
from models.base_models import MovieResponse
from utils.data_generator import DataGenerator


class TestMoviesApiWithDB:

    @allure.title("Создание фильма с проверкой в базе данных")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("API фильмов")
    @allure.story("Создание фильма с проверкой БД")
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_create_movie_db_check(self, super_admin, valid_genre_id, db_helper):
        movie_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)

        with allure.step("Создание фильма через API"):
            create_response = super_admin.api.movies_api.create_movie(movie_data, expected_status=201)
            created_movie = MovieResponse(**create_response.json())
            movie_id = created_movie.id
            allure.attach(
                f"ID созданного фильма: {movie_id}",
                name="ID фильма",
                attachment_type=allure.attachment_type.TEXT
            )

        try:
            with allure.step("Проверка наличия фильма в базе данных по ID"):
                db_movie = db_helper.get_movie_by_id(movie_id)
                assert db_movie is not None, f"Фильм с ID '{movie_id}' не найден в БД"

            with allure.step("Сравнение данных из API и базы данных"):
                assert db_movie.id == movie_id, "ID фильма в БД не совпадает с API"
                assert db_movie.name == movie_data["name"], "Название фильма не совпадает"
                assert db_movie.price == float(movie_data["price"]), "Цена фильма не совпадает"
                assert db_movie.description == movie_data["description"], "Описание фильма не совпадает"
                assert db_movie.location == movie_data["location"], "Локация фильма не совпадает"
                assert db_movie.published == movie_data["published"], "Статус публикации не совпадает"
                assert db_movie.genre_id == movie_data["genreId"], "ID жанра не совпадает"
                assert db_movie.image_url == movie_data.get("imageUrl"), "URL изображения не совпадает"

            with allure.step("Удаление фильма через API"):
                super_admin.api.movies_api.delete_movie(movie_id, expected_status=200)

            with allure.step("Проверка отсутствия фильма в БД после удаления"):
                db_movie_after_delete = db_helper.get_movie_by_id(movie_id)
                assert db_movie_after_delete is None, \
                    f"Фильм с ID '{movie_id}' все еще присутствует в БД после удаления"

            with allure.step("Проверка недоступности фильма через API"):
                super_admin.api.movies_api.get_movie_by_id(movie_id, expected_status=404)

        finally:
            with allure.step("Очистка тестовых данных из базы данных"):
                db_movie = db_helper.get_movie_by_id(movie_id)
                if db_movie:
                    db_helper.cleanup_test_data([db_movie])