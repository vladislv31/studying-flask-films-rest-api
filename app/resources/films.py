"""Module implements and connects resources for films."""

from flask_restful import Resource
from flask_login import login_required, current_user
from flask_pydantic import validate

from app.models import Film

from app import api

from app.utils.database.films import FilmsCRUD
from app.exceptions import ForeignKeyError, GenreIdError, FilmIdError

from app.schemas.films import FilmsQuerySchema, FilmBodySchema, FilmWithUserIdBodySchema

from app.utils.responses import successful_response_message, \
    bad_request_response_message, \
    unauthorized_request_response_message, \
    not_found_request_response_message, \
    internal_server_response_message
from app.utils.decorators import single_film_middleware


class FilmsResource(Resource):
    """/films route resource."""

    @validate()
    def get(self, query: FilmsQuerySchema):
        """Returns all the films.
        Supports:
            - filtering by:
                - director_id
                - range of premiere_date
                - genres
            - searching
            - sorting by:
                - rating
                - premiere_date
        """
        films = FilmsCRUD.read(query)

        return {"count": len(films), "result": [film.dict() for film in films]}

    @login_required
    @validate()
    def post(self, body: FilmBodySchema):
        """Adds film into database."""
        try:
            FilmsCRUD.create(FilmWithUserIdBodySchema.parse_obj(
                body.dict() | {"user_id": current_user.id}
            ))

        except GenreIdError as err:
            return bad_request_response_message(err)

        except ForeignKeyError as err:
            return bad_request_response_message(err)

        except Exception as ex:
            return internal_server_response_message()

        return successful_response_message("Film has been added.")


class SingleFilmResource(Resource):
    """/films/<int:film_id> route resource."""

    def get(self, film_id):
        """Returns specific film."""
        try:
            film = FilmsCRUD.read_one(film_id)

        except FilmIdError as err:
            return not_found_request_response_message(err)

        except Exception as ex:
            return internal_server_response_message()

        return film.dict()

    @login_required
    @single_film_middleware
    @validate()
    def put(self, film_id, body: FilmBodySchema):
        """Updates specific film."""
        try:
            FilmsCRUD.update(film_id, FilmWithUserIdBodySchema.parse_obj(
                body.dict() | {"user_id": current_user.id}
            ))

        except FilmIdError as err:
            return not_found_request_response_message(err)

        except Exception as ex:
            return internal_server_response_message()

        return successful_response_message("Film has been updated.")

    @login_required
    @single_film_middleware
    def delete(self, film_id):
        """Deletes specific film."""
        try:
            FilmsCRUD.delete(film_id)

        except FilmIdError as err:
            return not_found_request_response_message(err)

        except Exception as ex:
            return internal_server_response_message()

        return successful_response_message("Film has been deleted.")


api.add_resource(FilmsResource, "/films")
api.add_resource(SingleFilmResource, "/films/<int:film_id>")

