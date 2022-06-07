"""Module implements and connects resources for films."""

from flask import request
from flask_restful import Resource
from flask_login import login_required, current_user

from app import api
from app.domain.films import get_all_films, create_film, update_film, delete_film, get_one_film

from app.utils.exceptions import EntityIdError, GenreIdError
from app.utils.logging.films import log_created_film, log_updated_film, log_deleted_film

from app.utils.responses import successful_response_message, \
    bad_request_response_message, \
    not_found_request_response_message

from app.schemas.films import FilmsQuerySchema, FilmBodySchema, FilmWithUserIdBodySchema


class FilmsResource(Resource):
    """/films route resource."""

    def get(self):
        query = FilmsQuerySchema.parse_obj(request.args)
        films = get_all_films(query)
        return {
            "count": len(films),
            "result": [film.dict() for film in films]
        }

    @login_required
    def post(self):
        """Adds film into database."""
        try:
            body = FilmBodySchema.parse_obj(request.json)
            film = create_film(FilmWithUserIdBodySchema.parse_obj(
                body.dict() | {"user_id": current_user.id}
            ))

            log_created_film(film)

            return successful_response_message("Film has been added.", film.dict())

        except GenreIdError as err:
            return bad_request_response_message(err)


class SingleFilmsResource(Resource):

    def get(self, film_id):
        try:
            film = get_one_film(film_id)
            return film.dict()

        except EntityIdError as err:
            return not_found_request_response_message(err)

    @login_required
    def put(self, film_id):
        """Updates specific film."""
        try:
            body = FilmBodySchema.parse_obj(request.json)
            film = update_film(film_id, body)

            log_updated_film(film)

            return successful_response_message("Film has been updated.", film.dict())

        except EntityIdError as err:
            return not_found_request_response_message(err)

    @login_required
    def delete(self, film_id):
        try:
            delete_film(film_id)
            log_deleted_film(film_id)

            return successful_response_message("Film has been deleted.")

        except EntityIdError as err:
            return not_found_request_response_message(err)


api.add_resource(FilmsResource, "/films")
api.add_resource(SingleFilmsResource, "/films/<int:film_id>")

