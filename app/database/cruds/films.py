from app import app, db

from app.utils.exceptions import EntityIdError, GenreIdError, DirectorIdError
from app.models import Film, Genre, Director

from typing import Any

from app.database.cruds.base import BaseCRUD
from app.schemas.films import FilmsQuerySchema, FilmBodySchema, FilmWithUserIdBodySchema

from app.utils.orm import films_search_filter,  \
    films_director_filter, \
    films_premiere_date_filter, \
    films_genres_ids_filter, \
    films_ordering_sorting, \
    films_rating_filter


class FilmsCRUD(BaseCRUD[Film, Any, Any]):
    
    def __init__(self):
        super().__init__(Film, db.session)

    def create(self, data: FilmWithUserIdBodySchema) -> Film:
        try:
            if data.director_id:
                director = Director.query.filter_by(id=data.director_id).first()

                if not director:
                    raise DirectorIdError("director with such id not found: {}".format(data.director_id))

            film = Film(
                title=data.title,
                premiere_date=data.premiere_date,
                director_id=data.director_id,
                description=data.description,
                rating=data.rating,
                poster_url=data.poster_url,
                user_id=data.user_id
            )

            if data.genres_ids:
                for genre_id in set(data.genres_ids):
                    genre = Genre.query.filter_by(id=genre_id).first()

                    if not genre:
                        raise GenreIdError("genre with such id not found: {}".format(genre_id))

                    film.genres.append(genre)

            db.session.add(film)
            db.session.commit()

            return film

        except Exception as ex:
            db.session.rollback()
            raise ex

    def read(self, data: FilmsQuerySchema) -> list[Film]:
        search = data.search
        sort_order = data.sort_order
        sort_by = data.sort_by
        director_id = data.director_id
        rating = data.rating
        start_premiere_date = data.start_premiere_date
        end_premiere_date = data.end_premiere_date
        genres_ids = data.genres_ids
        page = data.page

        films_per_page = app.config["FILMS_PER_PAGE"]

        films_query = Film.query

        films_query = films_search_filter(films_query, search)
        films_query = films_director_filter(films_query, director_id)
        films_query = films_rating_filter(films_query, rating)
        films_query = films_premiere_date_filter(films_query, start_premiere_date, end_premiere_date)
        films_query = films_genres_ids_filter(films_query, genres_ids)
        films_query = films_ordering_sorting(films_query, sort_by, sort_order)

        films_query = films_query.paginate(page, films_per_page, False)
        films = films_query.items

        return films

    def update(self, id_: int, data: FilmBodySchema) -> Film:
        try:
            if data.director_id:
                director = Director.query.filter_by(id=data.director_id).first()

                if not director:
                    raise DirectorIdError("director with such id not found: {}".format(data.director_id))

            film = Film.query.filter_by(id=id_).first()

            if not film:
                raise EntityIdError("Film with such ID not found: {}".format(id_))

            film.title = data.title
            film.premiere_date = data.premiere_date
            film.director_id = data.director_id
            film.description = data.description
            film.rating = data.rating
            film.poster_url = data.poster_url

            if data.genres_ids:
                del film.genres[:]

                for genre_id in set(data.genres_ids):
                    genre = Genre.query.filter_by(id=genre_id).first()

                    if not genre:
                        raise GenreIdError("genre with such ID not found: {}.".format(genre_id))

                    film.genres.append(genre)
            
            db.session.add(film)
            db.session.commit()

            return film

        except Exception as err:
            db.session.rollback()
            raise err
