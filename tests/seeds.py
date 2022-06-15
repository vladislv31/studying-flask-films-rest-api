import random
from datetime import datetime

from faker import Faker

from werkzeug.security import generate_password_hash

from app import db
from app.database.models import Genre, Director, Film, User, Role

faker_ = Faker()

genres, directors_ids = [], []
used_genres = []


def db_seed():
    seed_role()
    seed_user()
    seed_genres()
    seed_directors()
    seed_films()


def seed_role():
    Role.query.delete()

    admin_role = Role(name="admin")
    user_role = Role(name="user")

    db.session.add(admin_role)
    db.session.add(user_role)

    db.session.add(admin_role)
    db.session.add(user_role)

    db.session.commit()


def seed_user():
    User.query.delete()

    admin = User(username="admin", password=generate_password_hash("123"), role_id=1)
    user = User(username="just_a_user", password=generate_password_hash("123"), role_id=2)

    db.session.add(admin)
    db.session.add(user)

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

    db.session.commit()


def seed_directors():
    Director.query.delete()

    for _ in range(20):
        first_name, last_name = faker_.name().split(" ")[:2]
        director = Director(
            first_name=first_name,
            last_name=last_name
        )
        db.session.add(director)
        db.session.flush()
        directors_ids.append(director.id)

    db.session.commit()


def seed_films():
    Film.query.delete()

    for film_number in range(1000):
        film = Film(
            title=faker_.sentence(nb_words=3)[:-1],
            premiere_date=faker_.date_between_dates(date_start=datetime(2005, 1, 1), date_end=datetime(2022, 1, 1)),
            description=faker_.text(),
            poster_url="https://example.com/image",
            rating=random.randrange(5, 11),
            director_id=random.choice(directors_ids),
            user_id=(film_number % 2) + 1
        )

        film_genres = genres[:]
        random.shuffle(film_genres)

        for _ in range(random.randrange(1, 5)):
            film.genres.append(film_genres.pop())

        db.session.add(film)

    db.session.commit()
