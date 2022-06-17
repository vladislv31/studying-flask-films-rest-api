from flask_restx import Resource, Namespace
from flask_login import login_required

from app.database.cruds.directors import DirectorsCRUD

from app.schemas.directors import DirectorCreateSchema, DirectorUpdateSchema
from app.domain.directors import get_all_directors, get_one_director, create_director, update_director, delete_director

from app.utils.exceptions import EntityIdError
from app.resources.utils.responses import successful_response_message, not_found_request_response_message
from app.utils.logging.directors import log_created_director, log_updated_director, log_deleted_director

from app.resources.parsers.directors import directors_body_parser
from app.resources.models.directors import director_response, directors_response, directors_body, \
    directors_add_response, directors_update_response, directors_delete_response


api = Namespace("directors", "Directors operations")


class DirectorsResource(Resource):

    @api.response(200, "Success", directors_response)
    def get(self):
        crud = DirectorsCRUD()
        directors = get_all_directors(crud)

        return {
            "count": len(directors),
            "result": [director.dict() for director in directors]
        }

    @login_required
    @api.expect(directors_body)
    @api.response(200, "Success", directors_add_response)
    @api.response(400, "Data validation error")
    @api.response(401, "Unauthenticated")
    def post(self):
        body = directors_body_parser.parse_args()

        crud = DirectorsCRUD()
        director = create_director(crud, DirectorCreateSchema.parse_obj(body))

        log_created_director(director)

        return successful_response_message("Director has been created.", director.dict())


@api.doc(params={"director_id": "Director ID"})
@api.response(404, "Director not found")
class SingleDirectorsResource(Resource):

    @api.response(200, "Success", director_response)
    def get(self, director_id):
        try:
            crud = DirectorsCRUD()
            director = get_one_director(crud, director_id)

            return director.dict()

        except EntityIdError as err:
            return not_found_request_response_message(err)

    @login_required
    @api.expect(directors_body)
    @api.response(200, "Success", directors_update_response)
    @api.response(400, "Data validation error")
    @api.response(401, "Unauthenticated")
    def put(self, director_id):
        try:
            body = directors_body_parser.parse_args()

            crud = DirectorsCRUD()
            director = update_director(crud, director_id, DirectorUpdateSchema.parse_obj(body))

            log_updated_director(director)

            return successful_response_message("Director has been updated.", director.dict())

        except EntityIdError as err:
            return not_found_request_response_message(err)

    @login_required
    @api.response(200, "Success", directors_delete_response)
    @api.response(401, "Unauthenticated")
    def delete(self, director_id):
        try:
            crud = DirectorsCRUD()
            delete_director(crud, director_id)

            log_deleted_director(director_id)

            return successful_response_message("Director has been deleted.")

        except EntityIdError as err:
            return not_found_request_response_message(err)


api.add_resource(DirectorsResource, "/")
api.add_resource(SingleDirectorsResource, "/<int:director_id>")
