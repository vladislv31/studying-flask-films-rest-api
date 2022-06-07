from flask import request
from flask_restful import Resource
from flask_login import login_required

from app import api
from app.schemas.genres import GenreCreateSchema, GenreUpdateSchema
from app.domain.genres import get_all_genres, get_one_genre, create_genre, update_genre, delete_genre

from app.utils.exceptions import GenreAlreadyExistsError, EntityIdError
from app.utils.responses import bad_request_response_message, successful_response_message, \
    not_found_request_response_message


class GenresResource(Resource):

    def get(self):
        genres = get_all_genres()
        return {
            "count": len(genres),
            "result": [genre.dict() for genre in genres]
        }

    @login_required
    def post(self):
        try:
            body = GenreCreateSchema.parse_obj(request.json)
            genre = create_genre(body)
            return successful_response_message("Genre has been created.", genre.dict())

        except GenreAlreadyExistsError as err:
            return bad_request_response_message(err)


class SingleGenresResource(Resource):

    def get(self, genre_id):
        try:
            genre = get_one_genre(genre_id)
            return genre.dict()

        except EntityIdError as err:
            return not_found_request_response_message(err)

    @login_required
    def put(self, genre_id):
        try:
            body = GenreUpdateSchema.parse_obj(request.json)
            genre = update_genre(genre_id, body)
            return successful_response_message("Genre has been updated.", genre.dict())

        except GenreAlreadyExistsError as err:
            return bad_request_response_message(err)

        except EntityIdError as err:
            return not_found_request_response_message(err)

    @login_required
    def delete(self, genre_id):
        try:
            delete_genre(genre_id)
            return successful_response_message("Genre has been deleted.")

        except EntityIdError as err:
            return not_found_request_response_message(err)
        

api.add_resource(GenresResource, "/genres")
api.add_resource(SingleGenresResource, "/genres/<int:genre_id>")
