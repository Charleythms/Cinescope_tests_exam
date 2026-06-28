import allure
import pytest


class TestUserApi:

    @allure.title("Создание нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("API пользователей")
    @allure.story("Создание пользователя")
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_create_user(self, super_admin, creation_user_data):
        with allure.step("Создание пользователя через API"):
            response = super_admin.api.user_api.create_user(creation_user_data).json()

        with allure.step("Проверка данных созданного пользователя"):
            assert response.get('id') and response['id'] != '', "ID должен быть не пустым"
            assert response.get('email') == creation_user_data['email'], "Email не совпадает"
            assert response.get('fullName') == creation_user_data['fullName'], "FullName не совпадает"
            assert response.get('roles', []) == creation_user_data['roles'], "Роли не совпадают"
            assert response.get('verified') is True, "Пользователь должен быть верифицирован"

        with allure.step("Удаление созданного пользователя"):
            super_admin.api.user_api.delete_user(user_id=response.get('id'))

    @allure.title("Получение пользователя по locator (ID и Email)")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("API пользователей")
    @allure.story("Получение пользователя")
    @pytest.mark.regression
    def test_get_user_by_locator(self, super_admin, creation_user_data):
        with allure.step("Создание пользователя"):
            created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()

        with allure.step("Получение пользователя по ID"):
            response_by_id = super_admin.api.user_api.get_user(created_user_response['id']).json()

        with allure.step("Получение пользователя по Email"):
            response_by_email = super_admin.api.user_api.get_user(creation_user_data['email']).json()

        with allure.step("Проверка совпадения данных"):
            assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
            assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
            assert response_by_id.get('email') == creation_user_data['email'], "Email не совпадает"
            assert response_by_id.get('fullName') == creation_user_data['fullName'], "FullName не совпадает"
            assert response_by_id.get('roles', []) == creation_user_data['roles'], "Роли не совпадают"
            assert response_by_id.get('verified') is True, "Пользователь должен быть верифицирован"

        with allure.step("Удаление пользователя"):
            super_admin.api.user_api.delete_user(user_id=created_user_response.get('id'))

    @allure.title("Проверка доступа обычного пользователя к данным другого пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("API пользователей")
    @allure.story("Контроль доступа")
    @pytest.mark.negative
    @pytest.mark.critical
    def test_get_user_by_id_common_user(self, common_user):
        with allure.step("Попытка получения данных пользователя обычным пользователем"):
            common_user.api.user_api.get_user(common_user.email, expected_status=403)