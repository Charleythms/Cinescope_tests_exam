import pytest
from models.base_models import MovieResponse


class TestMoviesApiFilters:

    @pytest.mark.smoke
    @pytest.mark.filters
    def test_filter_by_location(self, authenticated_admin):
        response = authenticated_admin.movies_api.get_movies(
            params={"locations": "SPB", "pageSize": 20},
            expected_status=200
        )
        data = response.json()

        for movie_data in data.get("movies", []):
            movie = MovieResponse(**movie_data)
            assert movie.location == "SPB"

    @pytest.mark.smoke
    @pytest.mark.filters
    def test_filter_by_genre(self, authenticated_admin):
        target_genre_id = 3

        response = authenticated_admin.movies_api.get_movies(
            params={"genreId": target_genre_id, "pageSize": 20},
            expected_status=200
        )
        data = response.json()

        for movie_data in data.get("movies", []):
            movie = MovieResponse(**movie_data)
            assert movie.genreId == target_genre_id