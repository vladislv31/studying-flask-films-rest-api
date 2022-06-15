import random
from datetime import datetime

from faker import Faker


faker_ = Faker()


def generate_director_id(client):
    directors_resp = client.get("/directors/")
    directors = directors_resp.json

    director_id = random.choice(directors["result"])["id"]

    return director_id


def generate_genres_ids(client):
    genres_resp = client.get("/genres/")
    genres = genres_resp.json

    genres_ids = []
    for _ in range(random.randrange(1, 6)):
        genres_ids.append(random.choice(genres["result"])["id"])

    return genres_ids


def generate_film_data(client):
    return {
        "title": faker_.sentence(nb_words=3)[:-1],
        "premiere_date": str(faker_.date_between_dates(date_start=datetime(2005, 1, 1), date_end=datetime(2022, 1, 1))),
        "description": faker_.text(),
        "poster_url": "https://example.com/image",
        "rating": random.randrange(1, 11),
        "director_id": generate_director_id(client),
        "genres_ids": generate_genres_ids(client)
    }


def generate_director_data():
    first_name, last_name = faker_.name().split(" ")[:2]
    return {
        "first_name": first_name,
        "last_name": last_name
    }
