"""Command manager."""

import random
from datetime import datetime

from faker import Faker

from app import app, db
from app.database.models import Genre, Director, Film, User


faker_ = Faker()

genres, directors_ids = [], []
used_genres = []


@app.cli.command("db-seed")
def db_seed():
    seed_genres()
    seed_directors()
    seed_films()

    db.session.commit()


def seed_genres():
    Genre.query.delete()

    for _ in range(20):
        genre_name = faker_.word()

        while genre_name in used_genres:
            genre_name = faker_.word()

        used_genres.append(genre_name)

        genre = Genre(name=genre_name.capitalize())
        db.session.add(genre)
        db.session.flush()
        genres.append(genre)


def seed_directors():
    Director.query.delete()

    for _ in range(15):
        first_name, last_name = faker_.name().split(" ")[:2]
        director = Director(
            first_name=first_name,
            last_name=last_name
        )
        db.session.add(director)
        db.session.flush()
        directors_ids.append(director.id)
    

def seed_films():
    Film.query.delete()

    for _ in range(200):
        film = Film(
            title=faker_.sentence(nb_words=3)[:-1],
            premiere_date=faker_.date_between_dates(date_start=datetime(2005, 1, 1), date_end=datetime(2022, 1, 1)),
            description=faker_.text(),
            poster_url="https://example.com/image",
            rating=random.randrange(5, 11),
            director_id=random.choice(directors_ids),
            user_id=User.query.first().id
        )

        film_genres = genres[:]
        random.shuffle(film_genres)

        for _ in range(random.randrange(1, 5)):
            film.genres.append(film_genres.pop())

        db.session.add(film)

