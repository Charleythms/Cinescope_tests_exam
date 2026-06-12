from faker import Faker

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