"""Module implements and connects resources for films."""

from flask_restful import Resource
from flask_login import login_required

from app import api, db
from app.models import Film

from app.parsers import film_body_parser, film_args_parser

from app.utils.db import get_all_films, add_film
from app.utils.responses import successful_response_message, bad_request_response_message


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
                genres_ids=args["genres_ids"])

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
            user_id=body["user_id"]
        )

        if result:
            return successful_response_message("Film has been added.")

        return bad_request_response_message(error)


class SingleFilmResource(Resource):
    """/films/<int:film_id> route resource."""

    def get(self, film_id):
        """Returns specific film."""
        film = Film.query.filter_by(id=film_id).first()

        return {
            "id": film.id,
            "title": film.title,
            "premiere_date": str(film.premiere_date),
            "director_id": film.director_id,
            "description": film.description,
            "rating": film.rating,
            "poster_url": film.poster_url,
            "user_id": film.user_id
        }

    def put(self, film_id):
        """Updates specific film."""
        parser = film_body_parser()
        args = parser.parse_args()

        film = Film.query.get_or_404(film_id)

        film.title = args["title"]
        film.premiere_date = args["premiere_date"]
        film.director_id = args["director_id"]
        film.description = args["description"]
        film.rating = args["rating"]
        film.poster_url = args["poster_url"]
        film.user_id = args["user_id"]

        db.session.add(film)
        db.session.commit()

        return successful_response_message("Film has been updated.")

    def delete(self, film_id):
        """Deletes specific film."""
        film = Film.query.get_or_404(film_id)

        db.session.delete(film)
        db.session.commit()

        return successful_response_message("Film has been deleted.")


api.add_resource(FilmsResource, "/films")
api.add_resource(SingleFilmResource, "/films/<int:film_id>")

