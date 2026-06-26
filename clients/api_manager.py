from clients.auth_api import AuthAPI
from clients.movies_api import MoviesApi, GenresApi
from clients.user_api import UserAPI


class ApiManager:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)
        self.movies_api = MoviesApi(session)
        self.genres_api = GenresApi(session)

    def close_session(self):
        if self.session:
            self.session.close()