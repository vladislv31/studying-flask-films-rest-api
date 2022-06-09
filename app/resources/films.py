"""Module implements and connects resources for films."""

from flask_restx import Resource, Namespace
from flask_login import login_required, current_user

from app.domain.films import get_all_films, create_film, update_film, delete_film, get_one_film

from app.utils.exceptions import EntityIdError, GenreIdError, DirectorIdError
from app.utils.logging.films import log_created_film, log_updated_film, log_deleted_film

from app.utils.responses import successful_response_message, \
    bad_request_response_message, \
    not_found_request_response_message

from app.schemas.films import FilmsQuerySchema, FilmBodySchema, FilmWithUserIdBodySchema

from app.resources.models.films import films_response, films_body, films_add_response, films_update_response, film_response, films_delete_response
from app.resources.parsers.films import films_query_parser, films_body_parser


api = Namespace("films", "Films operations")


@api.response(400, "Data validation error")
class FilmsResource(Resource):
    """Films resource."""

    @api.expect(films_query_parser)
    @api.response(200, "Success", films_response)
    def get(self):
        """Returns films list."""
        query = films_query_parser.parse_args()
        films = get_all_films(FilmsQuerySchema.parse_obj(query))
        return {
            "count": len(films),
            "result": [film.dict() for film in films]
        }

    @login_required
    @api.expect(films_body)
    @api.response(200, "Success", films_add_response)
    @api.response(401, "Unauthenticated")
    def post(self):
        """Adds film into database."""
        try:
            body = films_body_parser.parse_args()
            film = create_film(FilmWithUserIdBodySchema.parse_obj(
                body | {"user_id": current_user.id}
            ))

            log_created_film(film)

            return successful_response_message("Film has been created.", film.dict())

        except EntityIdError as err:
            return bad_request_response_message(err)


@api.doc(params={"film_id": "Film ID"})
@api.response(404, "Film not found")
class SingleFilmsResource(Resource):

    @api.response(200, "Success", film_response)
    def get(self, film_id):
        """Returns specific film."""
        try:
            film = get_one_film(film_id)
            return film.dict()

        except EntityIdError as err:
            return not_found_request_response_message(err)

    @login_required
    @api.expect(films_body)
    @api.response(200, "Success", films_update_response)
    @api.response(400, "Data validation error")
    @api.response(401, "Unauthenticated")
    def put(self, film_id):
        """Updates specific film."""
        try:
            body = films_body_parser.parse_args()
            film = update_film(film_id, FilmBodySchema.parse_obj(body))

            log_updated_film(film)

            return successful_response_message("Film has been updated.", film.dict())

        except (GenreIdError, DirectorIdError) as err:
            return bad_request_response_message(err)

        except EntityIdError as err:
            return not_found_request_response_message(err)

    @login_required
    @api.response(401, "Unauthenticated")
    @api.response(200, "Success", films_delete_response)
    def delete(self, film_id):
        """Deletes specific film."""
        try:
            delete_film(film_id)
            log_deleted_film(film_id)

            return successful_response_message("Film has been deleted.")

        except EntityIdError as err:
            return not_found_request_response_message(err)


api.add_resource(FilmsResource, "/")
api.add_resource(SingleFilmsResource, "/<int:film_id>")

