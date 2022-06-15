from app.domain.films import get_one_film, create_film, get_all_films
from app.database.models import Film, User, Director
from app.database.cruds.base import AbstractCRUD
from app.database.cruds.films import FilmsCRUD
from app.schemas.films import FilmWithUserIdBodySchema, FilmSchema, FilmsQuerySchema
from app.schemas.directors import DirectorSchema

import app.domain.films as films_domain_module


class FakeCRUD(AbstractCRUD):
    _films = []

    def create(self, data: FilmWithUserIdBodySchema):
        user = User(id=data.user_id, username="someone")
        director = Director(id=data.director_id, first_name="Someone", last_name="Famous") \
            if data.director_id else None

        film = Film(
            id=len(self._films) + 1,
            title=data.title,
            premiere_date=data.premiere_date,
            director_id=data.director_id,
            director=director,
            description=data.description,
            rating=data.rating,
            poster_url=data.poster_url,
            user_id=data.user_id,
            user=user
        )

        self._films.append(film)

        return FilmSchema.from_orm(film)

    def read_one(self, film_id: int):
        for film in self._films:
            if film.id == film_id:
                return FilmSchema.from_orm(film)
        return None


class MockedUser:

    def is_admin(self):
        return True


def test_added_film_director(monkeypatch):
    monkeypatch.setattr(films_domain_module, "current_user", MockedUser())

    crud = FakeCRUD()
    film = create_film(crud, FilmWithUserIdBodySchema.parse_obj({
        "title": "Film title",
        "rating": 10,
        "user_id": 1,
        "director_id": 1
    }))

    returned_film = get_one_film(crud, film.id)
    assert isinstance(returned_film.director, DirectorSchema)


def test_added_film_director_unknown(monkeypatch):
    monkeypatch.setattr(films_domain_module, "current_user", MockedUser())

    crud = FakeCRUD()
    film = create_film(crud, FilmWithUserIdBodySchema.parse_obj({
        "title": "Film title",
        "rating": 10,
        "user_id": 1
    }))

    returned_film = get_one_film(crud, film.id)
    assert returned_film.director == "unknown"
