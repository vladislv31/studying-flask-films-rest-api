"""Module implemets utils for working with database."""

from app.models import Film, Director, Genre, film_genres
from app.exceptions import GenreIdError, FilmIdError
from app import db

from sqlalchemy.exc import IntegrityError

from psycopg2.errors import ForeignKeyViolation


def add_film(**kwargs):
    """Adds film to database.
    Args:
        - title
        - premiere_date
        - director_id
        - description
        - rating
        - poster_url
        - user_id
        - genres_ids
    Returns:
        - True, False - if no errors
        - True, str - if there is error, second value - error message
    """
    is_commited = False

    try:
        film = Film(
            title=kwargs["title"],
            premiere_date=kwargs["premiere_date"],
            director_id=kwargs["director_id"],
            description=kwargs["description"],
            rating=kwargs["rating"],
            poster_url=kwargs["poster_url"],
            user_id=kwargs["user_id"]
        )

        if kwargs["genres_ids"]:
            for genre_id in kwargs["genres_ids"]:
                genre = Genre.query.filter_by(id=genre_id).first()

                if not genre:
                    raise GenreIndexError("genre with such index not found: {}".format(genre_id))

                film.genres.append(genre)

        db.session.add(film)
        db.session.commit()
        is_commited = True

    except GenreIndexError as err:
        return False, {"genres_ids": str(err)}

    except IntegrityError as err:
        return False, {"director_id": "director_id foreign key specified wrong."}

    finally:
        if not is_commited:
            db.session.rollback()

    return True, False


def update_film(**kwargs):
    """Updates film.
    Args:
        - user_id
        - title
        - premiere_date
        - director_id
        - description
        - rating
        - poster_url
        - user_id
        - genres_ids
    Returns:
        - True, False - if no errors
        - True, str - if there is error, second value - error message
    """
    is_commited = False

    try:
        film = Film.query.filter_by(id=kwargs["film_id"]).first()

        if not film:
            raise FilmIdError("Film with such ID not found: {}".format())

        film.title = kwargs["title"]
        film.premiere_date = kwargs["premiere_date"]
        film.director_id = kwargs["director_id"]
        film.description = kwargs["description"]
        film.rating = kwargs["rating"]
        film.poster_url = kwargs["poster_url"]

        if kwargs["genres_ids"]:
            del film.genres[:]

            for genre_id in kwargs["genres_ids"]:
                genre = Genre.query.filter_by(id=genre_id).first()

                if not genre:
                    raise GenreIdError("genre with such ID not found: {}.".format(genre_id))

                film.genres.append(genre)
        
        db.session.add(film)
        db.session.commit()
        is_commited = True

    except FilmIdError as err:
        return False, {"film_id": str(err)}

    except GenreIdError as err:
        return False, {"genres_ids": str(err)}

    except IntegrityError as err:
        return False, {"director_id": "director_id foreign key specified wrong."}

    except Exception as err:
        return False, {"message": str(err)}

    finally:
        if not is_commited:
            db.session.rollback()

    return True, False


def delete_film(film_id):
    is_commited = False

    try:
        film = Film.query.filter_by(id=film_id).first()

        if not film:
            raise FilmIdError("Film with such ID not found: {}".format())

        db.session.delete(film)
        db.session.commit()
        is_commited = True

    except FilmIdError as err:
        return False, {"film_id": str(err)}

    finally:
        if not is_commited:
            db.session.rollback()

    return True, False


def get_all_films(**kwargs):
    """Returns films from database.
    Args(every argument is not required):
        - search
        - sort_order
        - sort_by
        - director_id
        - start_premiere_date
        - end_premiere_date
        - genres_ids
    Returns:
        - list - list of films
    """
    search = kwargs.get("search", None)
    sort_order = kwargs.get("sort_order", None)
    sort_by = kwargs.get("sort_by", None)
    director_id = kwargs.get("director_id", None)
    start_premiere_date = kwargs.get("start_premiere_date", None)
    end_premiere_date = kwargs.get("end_premiere_date", None)
    genres_ids = kwargs.get("genres_ids", None)

    films_query = Film.query

    films_query = films_search_filter(films_query, search)
    films_query = films_director_filter(films_query, director_id)
    films_query = films_premiere_date_filter(films_query, start_premiere_date, end_premiere_date)
    films_query = films_genres_ids_filter(films_query, genres_ids)
    films_query = films_ordering_sorting(films_query, sort_by, sort_order)

    films_query = films_query.all()

    films = []

    for film in films_query:
        films.append({
            "id": film.id,
            "title": film.title,
            "premiere_date": str(film.premiere_date),

            "director": {
                "id": film.director.id,
                "name": f"{film.director.first_name} {film.director.last_name}"
            } if film.director else "unknown",

            "genres": [genre.name for genre in film.genres],
            "description": film.description,
            "rating": film.rating,
            "poster_url": film.poster_url,
            "user": {
                "id": film.user.id,
                "username": film.user.username
            }
        })

    return films


# orm helpers


def films_search_filter(query, search):
    if search:
        search_like = "%{}%".format(search)
        query = query.filter(Film.title.like(search_like))

    return query


def films_director_filter(query, director_id):
    if director_id:
        query = query.filter(Film.director_id == director_id)

    return query


def films_premiere_date_filter(query, start_premiere_date, end_premiere_date):
    if start_premiere_date:
        query = query.filter(Film.premiere_date >= start_premiere_date)

    if end_premiere_date:
        query = query.filter(Film.premiere_date <= end_premiere_date)

    return query


def films_genres_ids_filter(query, genres_ids):
    if genres_ids:
        query = query.filter(Film.genres.any(Genre.id.in_(genres_ids)))

    return query


def films_ordering_sorting(query, sort_by, sort_order):
    order_field = Film.id

    if sort_by == "rating":
        order_field = Film.rating
    elif sort_by == "premiere_date":
        order_field = Film.premiere_date

    order_by = order_field.asc()

    if sort_order == -1:
        order_by = order_field.desc()

    return query.order_by(order_by)

