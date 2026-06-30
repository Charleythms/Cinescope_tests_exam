import allure
import pytest
from faker import Faker
from models.pages.login_page import CinescopeLoginPage
from models.pages.movie_page import CinescopeMoviePage
faker = Faker()

@allure.epic('Тесты UI')
@allure.feature('Тест страницы фильмов')
@pytest.mark.UI
@pytest.mark.critical
class TestMoviePage:
    @allure.title('Тест написания отзыва')
    def test_post_review(self, page, movie_id, registered_user, review_text = 'good movie', rating = faker.random_int(1,5)):

        login_page = CinescopeLoginPage(page)
        movie_page = CinescopeMoviePage(page, movie_id)

        login_page.open()
        login_page.login(registered_user['email'], registered_user['password'])
        login_page.assert_error_was_pop_up()
        login_page.reload_page()

        movie_page.open()
        movie_page.write_review(review_text)
        movie_page.set_rating(rating)
        movie_page.post_review()

        movie_page.assert_allert_was_pop_up()
        movie_page.assert_review_was_posted(review_text)
        movie_page.assert_review_rating_correct(review_text, rating)