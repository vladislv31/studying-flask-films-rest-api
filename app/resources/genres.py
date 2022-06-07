from flask_pydantic import validate
from flask_restful import Resource
from flask_login import login_required

from app import api
from app.schemas.genres import GenreCreateSchema, GenreUpdateSchema
from app.domain.genres import get_all_genres, get_one_genre, create_genre, update_genre, delete_genre

from app.utils.exceptions import GenreAlreadyExistsError, EntityIdError

from app.utils.responses import bad_request_response_message, successful_response_message


class GenresResource(Resource):

    def get(self):
        return get_all_genres()

    @login_required
    @validate()
    def post(self, body: GenreCreateSchema):
        try:
            genre = create_genre(body)
            return successful_response_message("Genre has been created.", genre)

        except GenreAlreadyExistsError as err:
            return bad_request_response_message(err)


class SingleGenresResource(Resource):

    def get(self, genre_id):
        try:
            return get_one_genre(genre_id)

        except EntityIdError as err:
            return bad_request_response_message(err)

    @login_required
    @validate()
    def put(self, genre_id, body: GenreUpdateSchema):
        try:
            genre = update_genre(genre_id, body)

            return successful_response_message("Genre has been updated.", genre)

        except GenreAlreadyExistsError as err:
            return bad_request_response_message(err)

        except EntityIdError as err:
            return bad_request_response_message(err)

    @login_required
    def delete(self, genre_id):
        try:
            delete_genre(genre_id)
            return successful_response_message("Genre has been deleted.")

        except EntityIdError as err:
            return bad_request_response_message(err)
        

api.add_resource(GenresResource, "/genres")
api.add_resource(SingleGenresResource, "/genres/<int:genre_id>")

