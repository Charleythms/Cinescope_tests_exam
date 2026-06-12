import pytest


class TestMoviesApiFilters:

    @pytest.mark.smoke
    @pytest.mark.filters
    def test_filter_by_location(self, authenticated_admin):
        response = authenticated_admin.movies_api.get_movies(
            params={"locations": "SPB", "pageSize": 20},
            expected_status=200
        )
        data = response.json()
        for movie in data.get("movies", []):
            assert movie["location"] == "SPB"

    @pytest.mark.smoke
    @pytest.mark.filters
    def test_filter_by_genre(self, authenticated_admin):
        target_genre_id = 3 #поиск по фантастике

        response = authenticated_admin.movies_api.get_movies(
            params={"genreId": target_genre_id, "pageSize": 20},
            expected_status=200
        )
        data = response.json()

        for movie in data.get("movies", []):
            assert movie["genreId"] == target_genre_id, (
                f"Фильм {movie['id']} получил айди {movie['genreId']}, ожидалось {target_genre_id}"
            )