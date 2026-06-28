import allure
import pytest
import requests
from clients.api_manager import ApiManager
from models.base_models import RegisterUserResponse


class TestAuthApi:

    @allure.title("Регистрация нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("API аунтефикации")
    @allure.story("Регистрация пользователя")
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_register_user(self, super_admin, api_manager: ApiManager, test_user):
        with allure.step("Регистрация пользователя через API"):
            response = api_manager.auth_api.register_user(user_data=test_user)
            register_user_response = RegisterUserResponse(**response.json())

        with allure.step("Проверка данных зарегистрированного пользователя"):
            assert register_user_response.email == test_user.email, "Email не совпадает"
            assert register_user_response.fullName == test_user.fullName, "FullName не совпадает"

        with allure.step("Удаление созданного пользователя"):
            register_data = response.json()
            user_id = register_data['id']
            super_admin.api.user_api.delete_user(user_id=user_id, expected_status=200)

    @allure.title("Регистрация и логин пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("API аунтефикации")
    @allure.story("Регистрация пользователя")
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_register_and_login_user(self, api_manager, registration_user_data, super_admin):
        with allure.step("Регистрация пользователя"):
            response = api_manager.auth_api.register_user(registration_user_data, expected_status=201)
            register_user_response = RegisterUserResponse(**response.json())
            user_id = register_user_response.id

        with allure.step("Логин пользователя"):
            user_session = requests.Session()
            user_api_manager = ApiManager(user_session)

            login_response = user_api_manager.auth_api.login_user({
                "email": registration_user_data["email"],
                "password": registration_user_data["password"]
            }, expected_status=201)
            login_data = login_response.json()

        with allure.step("Проверка токенов в ответе"):
            assert "accessToken" in login_data, "Отсутствует accessToken"
            assert "refreshToken" in login_data, "Отсутствует refreshToken"

        with allure.step("Очистка тестовых данных"):
            super_admin.api.user_api.delete_user(user_id, expected_status=200)
            user_session.close()