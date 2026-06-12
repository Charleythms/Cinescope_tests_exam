import pytest
from utils.data_generator import DataGenerator

class TestMoviesApiNegative:

    @pytest.mark.negative
    @pytest.mark.critical
    def test_create_movie_missing_fields(self, authenticated_admin):
        invalid_fields = {"name": "test"}
        authenticated_admin.movies_api.create_movie(invalid_fields, expected_status=400)

    @pytest.mark.negative
    @pytest.mark.regression
    def test_create_movie_with_negative_price(self, authenticated_admin, valid_genre_id):
        movie_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)
        movie_data["price"] = -100
        authenticated_admin.movies_api.create_movie(movie_data, expected_status=400)

    @pytest.mark.negative
    def test_create_movie_with_invalid_loc(self, authenticated_admin, valid_genre_id):
        movie_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)
        movie_data["location"] = "INVALID/CITY"
        authenticated_admin.movies_api.create_movie(movie_data, expected_status=400)

    @pytest.mark.negative
    @pytest.mark.smoke
    def test_get_movie_by_noname_id(self, authenticated_admin):
        authenticated_admin.movies_api.get_movie_by_id(12312321, expected_status=404)

    @pytest.mark.negative
    def test_update_noname_movie(self, authenticated_admin):
        update_data = {"name": "Updated Name"}
        authenticated_admin.movies_api.update_movie(132123123, update_data, expected_status=404)

    @pytest.mark.negative
    def test_delete_noname_movie(self, authenticated_admin):
        authenticated_admin.movies_api.delete_movie(12312312, expected_status=404)

    @pytest.mark.negative
    @pytest.mark.regression
    def test_create_movie_with_empty_name(self, authenticated_admin, valid_genre_id):
        movie_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)
        movie_data["name"] = ""
        authenticated_admin.movies_api.create_movie(movie_data, expected_status=400)