import allure
import pytest

from models.pages.login_page import CinescopeLoginPage

@allure.epic('Тесты UI')
@allure.feature('Тест страницы входа')
@pytest.mark.UI
@pytest.mark.critical
class TestLoginPage:
     @allure.title('Тест успешного входа в систему')
     def test_login_by_ui(self, registered_user, page):

          login_page = CinescopeLoginPage(page)

          login_page.open()
          login_page.login(registered_user['email'], registered_user['password'])
          login_page.assert_error_was_pop_up()
          login_page.reload_page()

          login_page.assert_was_redirect_to_home_page()