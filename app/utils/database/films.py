from sqlalchemy.exc import IntegrityError


from app import app, db

from app.schemas.films import FilmWithUserIdBodySchema, FilmsQuerySchema, FilmSchema
from app.exceptions import GenreIdError, ForeignKeyError, FilmIdError
from app.models import Film, Genre
from app.utils.orm import films_search_filter,  \
        films_director_filter, \
        films_premiere_date_filter, \
        films_genres_ids_filter, \
        films_ordering_sorting


class FilmsCRUD:
    
    @staticmethod
    def create(data: FilmWithUserIdBodySchema) -> None:
        try:
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
                for genre_id in data.genres_ids:
                    genre = Genre.query.filter_by(id=genre_id).first()

                    if not genre:
                        raise GenreIdError("genre with such index not found: {}".format(genre_id))

                    film.genres.append(genre)

            db.session.add(film)
            db.session.commit()

        except IntegrityError as err:
            db.session.rollback()
            raise ForeignKeyError("director_id foreign key specified wrong.")

        except Exception as ex:
            db.session.rollback()
            raise ex

    @staticmethod
    def read(data: FilmsQuerySchema) -> list[FilmSchema]:
        search = data.search
        sort_order = data.sort_order
        sort_by = data.sort_by
        director_id = data.director_id
        start_premiere_date = data.start_premiere_date
        end_premiere_date = data.end_premiere_date
        genres_ids = data.genres_ids
        page = data.page

        films_per_page = app.config["FILMS_PER_PAGE"]

        films_query = Film.query

        films_query = films_search_filter(films_query, search)
        films_query = films_director_filter(films_query, director_id)
        films_query = films_premiere_date_filter(films_query, start_premiere_date, end_premiere_date)
        films_query = films_genres_ids_filter(films_query, genres_ids)
        films_query = films_ordering_sorting(films_query, sort_by, sort_order)

        films_query = films_query.paginate(page, films_per_page, False)
        films_items = films_query.items

        films = []

        for film in films_items:
            films.append(FilmSchema.from_orm(film))

        return films

    @staticmethod
    def read_one(film_id: int) -> FilmSchema:
        film = Film.query.filter_by(id=film_id).first()

        if not film:
            raise FilmIdError("Film with such id not found: {}".format(film_id))

        return FilmSchema.from_orm(film)

    @staticmethod
    def update(film_id: int, data: FilmWithUserIdBodySchema) -> None:
        try:
            film = Film.query.filter_by(id=film_id).first()

            if not film:
                raise FilmIdError("Film with such ID not found: {}".format(data.id))

            film.title = data.title
            film.premiere_date = data.premiere_date
            film.director_id = data.director_id
            film.description = data.description
            film.rating = data.rating
            film.poster_url = data.poster_url
            film.user_id = data.user_id

            if data.genres_ids:
                del film.genres[:]

                for genre_id in data.genres_ids:
                    genre = Genre.query.filter_by(id=genre_id).first()

                    if not genre:
                        raise GenreIdError("genre with such ID not found: {}.".format(genre_id))

                    film.genres.append(genre)
            
            db.session.add(film)
            db.session.commit()
            is_commited = True

        except IntegrityError as err:
            db.session.rollback()
            raise ForeignKeyError("director_id foreign key specified wrong.")

        except Exception as err:
            db.session.rollback()
            raise err

    @staticmethod
    def delete(film_id: int) -> None:
        film = Film.query.filter_by(id=film_id).first()

        if not film:
            raise FilmIdError("Film with such ID not found: {}".format(film_id))

        db.session.delete(film)
        db.session.commit()

