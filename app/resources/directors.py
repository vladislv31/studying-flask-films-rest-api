from flask import request
from flask_restful import Resource
from flask_login import login_required

from app import api
from app.schemas.directors import DirectorCreateSchema, DirectorUpdateSchema
from app.domain.directors import get_all_directors, get_one_director, create_director, update_director, delete_director

from app.utils.exceptions import EntityIdError
from app.utils.responses import successful_response_message, not_found_request_response_message
from app.utils.logging.directors import log_created_director, log_updated_director, log_deleted_director


class DirectorsResource(Resource):

    def get(self):
        directors = get_all_directors()
        return {
            "count": len(directors),
            "result": [director.dict() for director in directors]
        }

    @login_required
    def post(self):
        body = DirectorCreateSchema.parse_obj(request.json)
        director = create_director(body)

        log_created_director(director)

        return successful_response_message("Director has been created.", director.dict())


class SingleDirectorsResource(Resource):

    def get(self, director_id):
        try:
            director = get_one_director(director_id)
            return director.dict()

        except EntityIdError as err:
            return not_found_request_response_message(err)

    @login_required
    def put(self, director_id):
        try:
            body = DirectorUpdateSchema.parse_obj(request.json)
            director = update_director(director_id, body)

            log_updated_director(director)

            return successful_response_message("Director has been updated.", director.dict())

        except EntityIdError as err:
            return not_found_request_response_message(err)

    @login_required
    def delete(self, director_id):
        try:
            delete_director(director_id)
            log_deleted_director(director_id)

            return successful_response_message("Director has been deleted.")

        except EntityIdError as err:
            return not_found_request_response_message(err)


api.add_resource(DirectorsResource, "/directors")
api.add_resource(SingleDirectorsResource, "/directors/<int:director_id>")

