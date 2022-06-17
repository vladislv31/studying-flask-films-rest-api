from flask_restx import Resource, Namespace
from flask_login import login_required

from app.database.cruds.genres import GenresCRUD
from app.schemas.genres import GenreCreateSchema, GenreUpdateSchema
from app.domain.genres import get_all_genres, get_one_genre, create_genre, update_genre, delete_genre

from app.utils.exceptions import GenreAlreadyExistsError, EntityIdError
from app.resources.utils.responses import bad_request_response_message, successful_response_message, \
    not_found_request_response_message

from app.utils.logging.genres import log_created_genre, log_updated_genre, log_deleted_genre

from app.resources.models.genres import genres_response, genres_body, genres_add_response, genres_update_response, \
    genres_delete_response, genre_response
from app.resources.parsers.genres import genres_body_parser


api = Namespace("genres", "Genres operations")


class GenresResource(Resource):

    @api.response(200, "Success", genres_response)
    def get(self):
        crud = GenresCRUD()
        genres = get_all_genres(crud)

        return {
            "count": len(genres),
            "result": [genre.dict() for genre in genres]
        }

    @login_required
    @api.expect(genres_body)
    @api.response(200, "Success", genres_add_response)
    @api.response(400, "Data validation error")
    @api.response(401, "Unauthenticated")
    def post(self):
        try:
            body = genres_body_parser.parse_args()

            crud = GenresCRUD()
            genre = create_genre(crud, GenreCreateSchema.parse_obj(body))

            log_created_genre(genre)

            return successful_response_message("Genre has been created.", genre.dict())

        except GenreAlreadyExistsError as err:
            return bad_request_response_message(err)


@api.doc(params={"genre_id": "Genre ID"})
@api.response(404, "Genre not found")
class SingleGenresResource(Resource):

    @api.response(200, "Success", genre_response)
    def get(self, genre_id):
        try:
            crud = GenresCRUD()
            genre = get_one_genre(crud, genre_id)

            return genre.dict()

        except EntityIdError as err:
            return not_found_request_response_message(err)

    @login_required
    @api.expect(genres_body)
    @api.response(200, "Success", genres_update_response)
    @api.response(400, "Data validation error")
    @api.response(401, "Unauthenticated")
    def put(self, genre_id):
        try:
            body = genres_body_parser.parse_args()

            crud = GenresCRUD()
            genre = update_genre(crud, genre_id, GenreUpdateSchema.parse_obj(body))

            log_updated_genre(genre)

            return successful_response_message("Genre has been updated.", genre.dict())

        except GenreAlreadyExistsError as err:
            return bad_request_response_message(err)

        except EntityIdError as err:
            return not_found_request_response_message(err)

    @login_required
    @api.response(200, "Success", genres_delete_response)
    @api.response(401, "Unauthenticated")
    def delete(self, genre_id):
        try:
            crud = GenresCRUD()
            delete_genre(crud, genre_id)

            log_deleted_genre(genre_id)

            return successful_response_message("Genre has been deleted.")

        except EntityIdError as err:
            return not_found_request_response_message(err)


api.add_resource(GenresResource, "/")
api.add_resource(SingleGenresResource, "/<int:genre_id>")
