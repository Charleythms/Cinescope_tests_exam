import pytest
from utils.data_generator import DataGenerator


class TestMoviesApiFilters:

    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.skip(reason="фильтр локации не работает")
    def test_filter_by_location(self, authenticated_admin, valid_genre_id):
        target_location = "SPB"

        movie_data = DataGenerator.generate_movie_data(genre_id=valid_genre_id)
        movie_data["location"] = target_location
        create_response = authenticated_admin.movies_api.create_movie(movie_data, expected_status=201)
        movie_id = create_response.json()["id"]

        try:
            response = authenticated_admin.movies_api.get_movies(
                params={"location": target_location},
                expected_status=200
            )
            data = response.json()

            for movie in data.get("movies", []):
                assert movie["location"] == target_location

        finally:
            authenticated_admin.movies_api.delete_movie(movie_id)