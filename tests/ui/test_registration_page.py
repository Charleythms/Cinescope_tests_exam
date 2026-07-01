import allure
import pytest

from models.pages.register_page import CinescopeRegisterPage
from utils.data_generator import DataGenerator

@allure.epic('Тесты UI')
@allure.feature('Тест страницы регистрации')
@pytest.mark.UI
@pytest.mark.critical
class TestRegisterPage:
    @allure.title('Тест регистрации')
    def test_register_by_ui(self, page):
        random_email = DataGenerator.generate_random_email()
        random_name = DataGenerator.generate_random_name()
        random_password = DataGenerator.generate_random_password()

        register_page = CinescopeRegisterPage(page)

        register_page.open()
        register_page.register(f"PlaywrightTest {random_name}", random_email, random_password, random_password)

        register_page.assert_was_redirect_to_login_page()

        register_page.assert_allert_was_pop_up()