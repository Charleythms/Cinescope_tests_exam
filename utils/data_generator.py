from datetime import datetime
from faker import Faker
import random
import string


faker = Faker()


class DataGenerator:

    @staticmethod
    def generate_random_genre():
        return {"name": faker.word().capitalize()}

    @classmethod
    def generate_movie_data(cls, genre_id=None, **kwargs):
        movie_data = {
            "name": faker.catch_phrase(),
            "description": faker.paragraph(nb_sentences=3),
            "price": faker.random_int(min=100, max=5000),
            "location": faker.random_element(elements=["MSK", "SPB"]),
            "published": faker.boolean(),
            "genreId": genre_id or faker.random_int(min=1, max=20),
            "imageUrl": faker.image_url()
        }
        movie_data.update(kwargs)
        return movie_data

    @classmethod
    def generate_random_email(cls):
        return faker.email()

    @classmethod
    def generate_random_name(cls):
        name = faker.name()
        name = ''.join(c for c in name if c.isalpha() or c == ' ')
        return name.strip()

    @staticmethod
    def generate_random_password():
        letters = random.choice(string.ascii_letters)
        digits = random.choice(string.digits)

        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return "".join(password)

    @staticmethod
    def generate_user_data() -> dict:
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }