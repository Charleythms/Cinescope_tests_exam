import pytest
from utils.data_generator import DataGenerator


class TestMoviesApiPositive:

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_movies(self, authenticated_admin):
        response = authenticated_admin.movies_api.get_movies(expected_status=200)
        data = response.json()

        assert "movies" in data
        assert "count" in data
        assert "page" in data
        assert "pageSize" in data
        assert "pageCount" in data

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_create_movie(self, authenticated_admin, valid_genre_id):
        movie_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)
        response = authenticated_admin.movies_api.create_movie(movie_data)
        created_movie = response.json()

        assert created_movie["name"] == movie_data["name"]
        assert created_movie["description"] == movie_data["description"]
        assert created_movie["price"] == movie_data["price"]
        assert created_movie["location"] == movie_data["location"]
        assert created_movie["published"] == movie_data["published"]
        assert created_movie["genreId"] == movie_data["genreId"]
        assert "id" in created_movie
        movie_id = response.json()["id"]

        authenticated_admin.movies_api.delete_movie(created_movie["id"])
        assert authenticated_admin.movies_api.get_movie_by_id(created_movie['id'], expected_status=404).status_code == 404

    @pytest.mark.regression
    def test_get_movie_by_id(self, authenticated_admin, valid_genre_id):
        movie_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)
        create_response = authenticated_admin.movies_api.create_movie(movie_data, expected_status=201)
        created_movie = create_response.json()
        movie_id = created_movie["id"]

        fetched_movie = authenticated_admin.movies_api.get_movie_by_id(movie_id, expected_status=200).json()

        assert fetched_movie["id"] == movie_id
        assert fetched_movie["name"] == movie_data["name"]
        assert fetched_movie["description"] == movie_data["description"]
        assert fetched_movie["price"] == movie_data["price"]
        assert fetched_movie["location"] == movie_data["location"]
        assert fetched_movie["published"] == movie_data["published"]
        assert fetched_movie["genreId"] == movie_data["genreId"]

        authenticated_admin.movies_api.delete_movie(movie_id)

    @pytest.mark.regression
    def test_update_movie(self, authenticated_admin, valid_genre_id):
        movie_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)
        create_response = authenticated_admin.movies_api.create_movie(movie_data, expected_status=201)
        movie_id = create_response.json()["id"]
        try:
            updated_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)
            updated_movie = authenticated_admin.movies_api.update_movie(movie_id, updated_data,  expected_status=200).json()

            assert updated_movie["id"] == movie_id
            assert updated_movie["name"] == updated_data["name"]
            assert updated_movie["description"] == updated_data["description"]
            assert updated_movie["price"] == updated_data["price"]
            assert updated_movie["location"] == updated_data["location"]
            assert updated_movie["published"] == updated_data["published"]
            assert updated_movie["genreId"] == updated_data["genreId"]

        finally:
            authenticated_admin.movies_api.delete_movie(movie_id)

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_delete_movie(self, authenticated_admin, valid_genre_id):
        movie_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)
        create_response = authenticated_admin.movies_api.create_movie(movie_data, expected_status=201)
        movie_id = create_response.json()["id"]

        assert authenticated_admin.movies_api.delete_movie(movie_id).status_code == 200
        assert authenticated_admin.movies_api.get_movie_by_id(movie_id, expected_status=404).status_code == 404