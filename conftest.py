import requests
import pytest
from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator
from config.test_data import AdminCredentials


@pytest.fixture(scope="session")
def session():
    with requests.Session() as http_session:
        yield http_session


@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)


@pytest.fixture(scope="session")
def authenticated_admin(api_manager):
    api_manager.auth_api.authenticate((AdminCredentials.EMAIL, AdminCredentials.PASSWORD))
    return api_manager


@pytest.fixture(scope="function")
def valid_genre_id(authenticated_admin):
    response = authenticated_admin.genres_api.get_genres(need_logging=False)
    genres = response.json()
    created_genre = False

    if not genres:
        genre_data = DataGenerator.generate_random_genre()
        genre_response = authenticated_admin.genres_api.create_genre(genre_data)
        genre_id = genre_response.json()["id"]
        created_genre = True
    else:
        genre_id = genres[0]["id"]

    yield genre_id

    if created_genre:
        authenticated_admin.genres_api.delete_genre(genre_id)