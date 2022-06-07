"""Command manager."""

import random
from datetime import datetime

from faker import Faker

from werkzeug.security import generate_password_hash

from app import app, db
from app.models import Genre, Director, Film, User, Role


faker_ = Faker()

genres, directors_ids = [], []
used_genres = []
admin_role_id = None
admin_user_id = None


@app.cli.command("db-seed")
def db_seed():
    seed_role()
    seed_user()
    seed_genres()
    seed_directors()
    seed_films()

    db.session.commit()


def seed_role():
    global admin_role_id

    print("Checking admin role existing...")
    if not Role.query.filter_by(name="admin").first():
        role = Role(name="admin")

        db.session.add(role)
        db.session.commit()
        db.session.refresh(role)

        admin_role_id = role.id
        print("Added admin role(id={})".format(role.id))
    else:
        admin_role_id = Role.query.filter_by(name="admin").first().id
        print("Admin role already exists.")

    print("Checking admin role existing...")
    if not Role.query.filter_by(name="user").first():
        role = Role(name="user")

        db.session.add(role)
        db.session.commit()
        db.session.refresh(role)

        print("Added users role(id={})".format(role.id))
    else:
        print("User role already exists.")


def seed_user():
    name = faker_.name().split(" ")
    username = "{}_{}_{}".format(name[0], name[1], faker_.pyint())
    password_hash = generate_password_hash("123")

    user = User(username=username, password=password_hash, role_id=admin_role_id)

    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)

    global admin_user_id
    admin_user_id = user.id

    print("Added admin user:")
    print("\tusername: {}".format(username))
    print("\tpassword: 123")


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

    print("Added 20 genres")


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

    print("Added 15 directors")
    

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
            user_id=admin_user_id
        )

        film_genres = genres[:]
        random.shuffle(film_genres)

        for _ in range(random.randrange(1, 5)):
            film.genres.append(film_genres.pop())

        db.session.add(film)

    print("Added 200 films")
