"""Command manager."""

import random

from app import app, db
from app.models import Genre, Director, Film, User


genres = [
    "Боевик",
    "Комедия",
    "Вестерн",
    "Гангстерский фильм",
    "Детектив",
    "Драма",
    "Исторический фильм",
    "Мелодрама"
]

directors = [
    "Сэм Рейми",
    "Энтони Руссо",
    "Джон Уотсс",
    "Алан Тейлор",
    "Джеймс Кэмерон",
    "Марк Уэбб",
    "Шейн Блэк",
    "Джоан Роулинг"
]

films = [
    "Человек-паук",
    "Железный человек",
    "Халк",
    "Тор",
    "Мстители",
    "Терминатор",
    "Гарри Поттер",
    "Первый мститель",
    "Черная вдова",
    "Человек-муравей"
]

genres_rows, directors_ids = [], []


@app.cli.command("db-seed")
def db_seed():
    seed_genres()
    seed_directors()
    seed_films()

    db.session.commit()


def seed_genres():
    Genre.query.delete()

    for genre_name in genres:
        genre = Genre(name=genre_name)
        db.session.add(genre)
        db.session.flush()
        genres_rows.append(genre)


def seed_directors():
    Director.query.delete()

    for director_name in directors:
        director = Director(
            first_name=director_name.split(" ")[0],
            last_name=director_name.split(" ")[1]
        )
        db.session.add(director)
        db.session.flush()
        directors_ids.append(director.id)
    

def seed_films():
    Film.query.delete()

    for film_title in films:
        for film_number in range(1, 6):
            film = Film(
                title=f"{film_title} {film_number}",
                premiere_date=f"{random.randrange(2000, 2022)}-{random.randrange(1, 13)}-{random.randrange(1, 28)}",
                description="Описание фильма...",
                poster_url="https://i.picsum.photos/id/222/200/300.jpg?hmac=owJZdOfXwkUqJHbR-MjF56GoNKbFIp3qGeGkkBS3Ei0",
                rating=random.randrange(5, 11),
                director_id=random.choice(directors_ids),
                user_id=User.query.first().id
            )

            for _ in range(random.randrange(1, 5)):
                film.genres.append(random.choice(genres_rows))

            db.session.add(film)

