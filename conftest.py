import requests
import pytest
from clients.api_manager import ApiManager
from config.base_urls import AUTH_BASE_URL
from config.test_data import SuperAdminCreds
from entities.roles import Roles
from entities.user import User
from models.base_models import TestUser
from utils.data_generator import DataGenerator
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper


@pytest.fixture(scope="function")
def created_test_user(db_helper):
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

@pytest.fixture
def db_helper(db_session):
    return DBHelper(db_session)

@pytest.fixture
def db_session():
    session = get_db_session()
    yield session
    session.close()
# ==================== СЕССИИ И API МЕНЕДЖЕРЫ ====================

@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)


@pytest.fixture(scope="session")
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture(scope="session")
def authenticated_admin(api_manager):
    api_manager.auth_api.authenticate((SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD))
    return api_manager


# ==================== ПОЛЬЗОВАТЕЛИ ====================

@pytest.fixture(scope="session")
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session
    )

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture
def admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.ADMIN.value],
        new_session
    )
    super_admin.api.user_api.create_user(creation_user_data)
    admin.api.auth_api.authenticate(admin.creds)
    return admin
    
@pytest.fixture(scope="function")
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


# ==================== ТЕСТОВЫЕ ДАННЫЕ ====================

@pytest.fixture(scope="function")
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )


@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.model_dump()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data


@pytest.fixture(scope="function")
def registration_user_data():
    random_password = DataGenerator.generate_random_password()

    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }


@pytest.fixture
def registered_user():
    user_data = {
        "email": "unique_email@mail.com",
        "fullName": "Mr Uniqueness Unique",
        "password": "Unique_password12345",
        "passwordRepeat": "Unique_password12345"
    }
    requests.post(f'{AUTH_BASE_URL}/register', json=user_data)
    return {
        'email': user_data['email'],
        'password': user_data['password']
    }


# ==================== ЖАНРЫ ====================

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