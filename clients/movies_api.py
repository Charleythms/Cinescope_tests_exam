from custom_requester.custom_requester import CustomRequester
from config.base_urls import API_BASE_URL


class MoviesApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=API_BASE_URL)

    def get_movies(self, params=None, expected_status=200):
        return self.send_request("GET", "/movies", params=params, expected_status=expected_status)

    def create_movie(self, movie_data, expected_status=201):
        return self.send_request("POST", "/movies", data=movie_data, expected_status=expected_status)

    def get_movie_by_id(self, movie_id, expected_status=200):
        return self.send_request("GET", f"/movies/{movie_id}", expected_status=expected_status)

    def update_movie(self, movie_id, update_data, expected_status=200):
        return self.send_request("PATCH", f"/movies/{movie_id}", data=update_data, expected_status=expected_status)

    def delete_movie(self, movie_id, expected_status=200):
        return self.send_request("DELETE", f"/movies/{movie_id}", expected_status=expected_status)


class GenresApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=API_BASE_URL)

    def get_genres(self, expected_status=200, need_logging=False):
        return self.send_request("GET", "/genres", expected_status=expected_status, need_logging=need_logging)

    def create_genre(self, genre_data, expected_status=201):
        return self.send_request("POST", "/genres", data=genre_data, expected_status=expected_status)

    def delete_genre(self, genre_id, expected_status=200):
        return self.send_request("DELETE", f"/genres/{genre_id}", expected_status=expected_status)