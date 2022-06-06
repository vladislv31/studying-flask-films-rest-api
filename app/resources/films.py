"""Module implements and connects resources for films."""

from flask_restful import Resource
from flask_login import login_required, current_user
from flask_pydantic import validate

from app import api, db
from app.domain.films import get_all_films, create_film, update_film, delete_film, get_one_film

from app.utils.exceptions import EntityIdError


from app.utils.responses import successful_response_message, \
    bad_request_response_message, \
    not_found_request_response_message, \
    internal_server_response_message

from app.database.schemas.films import FilmSchema, FilmsQuerySchema, FilmBodySchema, FilmWithUserIdBodySchema


class FilmsResource(Resource):
    """/films route resource."""

    @validate()
    def get(self, query: FilmsQuerySchema):
        films = get_all_films(query)
        return films

    @login_required
    @validate()
    def post(self, body: FilmBodySchema):
        """Adds film into database."""
        try:
            film = create_film(FilmWithUserIdBodySchema.parse_obj(
                body.dict() | {"user_id": current_user.id}
            ))

            return successful_response_message("Film has been added.", film)

        except EntityIdError as err:
            return bad_request_response_message(err)


class SingleFilmsResource(Resource):

    def get(self, film_id):
        try:
            film = get_one_film(film_id)

            return film

        except EntityIdError as err:
            return bad_request_response_message(err)

    @login_required
    @validate()
    def put(self, film_id, body: FilmBodySchema):
        """Updates specific film."""
        try:
            film =  update_film(film_id, body)

            return successful_response_message("Film has been updated.", film)

        except EntityIdError as err:
            return not_found_request_response_message(err)

    @login_required
    def delete(self, film_id):
        try:
            delete_film(film_id)

            return successful_response_message("Film has been deleted.")

        except EntityIdError as err:
            return bad_request_response_message(err)


api.add_resource(FilmsResource, "/films")
api.add_resource(SingleFilmsResource, "/films/<int:film_id>")

