"""Module implements and connects resources for films."""

from flask_restful import Resource
from flask_login import login_required, current_user

from app import api, db
from app.models import Film

from app.parsers import film_body_parser, film_args_parser

from app.utils.db import get_all_films, get_film_by_id, add_film, update_film, delete_film
from app.utils.responses import successful_response_message, \
    bad_request_response_message, \
    unauthorized_request_response_message, \
    not_found_request_response_message
from app.utils.decorators import single_film_middleware


class FilmsResource(Resource):
    """/films route resource."""

    def get(self):
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
        parser = film_args_parser()
        args = parser.parse_args()

        films = get_all_films(search=args["search"],
                sort_order=args["sort_order"],
                sort_by=args["sort_by"],
                director_id=args["director_id"],
                start_premiere_date=args["start_premiere_date"],
                end_premiere_date=args["end_premiere_date"],
                genres_ids=args["genres_ids"],
                page=args["page"])

        return {"count": len(films), "result": films}

    @login_required
    def post(self):
        """Adds film into database."""
        parser = film_body_parser()
        body = parser.parse_args()

        result, error = add_film(
            title=body["title"],
            premiere_date=body["premiere_date"],
            director_id=body["director_id"],
            description=body["description"],
            rating=body["rating"],
            poster_url=body["poster_url"],
            user_id=current_user.id,
            genres_ids=body["genres_ids"]
        )

        if result:
            return successful_response_message("Film has been added.")

        return bad_request_response_message(error)


class SingleFilmResource(Resource):
    """/films/<int:film_id> route resource."""

    def get(self, film_id):
        """Returns specific film."""
        film, error = get_film_by_id(film_id)

        if film:
            return film

        return bad_request_response_message(error)

    @login_required
    @single_film_middleware
    def put(self, film_id):
        """Updates specific film."""
        parser = film_body_parser()
        body = parser.parse_args()

        result, error = update_film(
            film_id=film_id,
            title=body["title"],
            premiere_date=body["premiere_date"],
            director_id=body["director_id"],
            description=body["description"],
            rating=body["rating"],
            poster_url=body["poster_url"],
            user_id=current_user.id,
            genres_ids=body["genres_ids"]
        )

        if result:
            return successful_response_message("Film has been updated.")

        return bad_request_response_message(error)

    @login_required
    @single_film_middleware
    def delete(self, film_id):
        """Deletes specific film."""
        result, error = delete_film(film_id)

        if result:
            return successful_response_message("Film has been deleted.")

        return successful_response_message(error)


api.add_resource(FilmsResource, "/films")
api.add_resource(SingleFilmResource, "/films/<int:film_id>")

