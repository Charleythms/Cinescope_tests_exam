import requests

from clients.api_manager import ApiManager
from models.base_models import RegisterUserResponse


class TestAuthApi:

    def test_register_user(self, super_admin, api_manager: ApiManager, test_user):

        response = api_manager.auth_api.register_user(user_data=test_user)
        register_user_response = RegisterUserResponse(**response.json())

        assert register_user_response.email == test_user.email, "Email не совпадает"
        assert register_user_response.fullName == test_user.fullName, "FullName не совпадает"

        register_data = response.json()
        user_id = register_data['id']
        super_admin.api.user_api.delete_user(user_id=user_id, expected_status=200)

    def test_register_and_login_user(self, api_manager, registration_user_data, super_admin):
        response = api_manager.auth_api.register_user(registration_user_data, expected_status=201)
        register_user_response = RegisterUserResponse(**response.json())
        user_id = register_user_response.id

        user_session = requests.Session()
        user_api_manager = ApiManager(user_session)

        login_response = user_api_manager.auth_api.login_user({
            "email": registration_user_data["email"],
            "password": registration_user_data["password"]
        }, expected_status=201)
        login_data = login_response.json()
        assert "accessToken" in login_data
        assert "refreshToken" in login_data

        super_admin.api.user_api.delete_user(user_id, expected_status=200)
        user_session.close()