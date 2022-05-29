from flask_restful import Resource

from app import api, db
from app.models import Film, Director

from app.parsers import film_args_parser 

from app.utils.db import get_all_films
from app.utils.responses import successful_response_message


class FilmsResource(Resource):

    def get(self):
        films = get_all_films()

        return {"count": len(films), "result": films}

    def post(self):
        parser = film_args_parser()
        args = parser.parse_args()

        film = Film(
            title=args["title"],
            premiere_date=args["premiere_date"],
            director_id=args["director_id"],
            description=args["description"],
            rating=args["rating"],
            poster_url=args["poster_url"],
            user_id=args["user_id"]
        )

        db.session.add(film)
        db.session.commit()

        return successful_response_message("Film has been added.")

class SingleFilmResource(Resource):

    def get(self, film_id):
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
        parser = film_args_parser()
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

        return successful_response_message("Film has been added.")

    def delete(self, film_id):
        film = Film.query.get_or_404(film_id)

        db.session.delete(film)
        db.session.commit()

        return successful_response_message("Film has been added.")


api.add_resource(FilmsResource, "/films")
api.add_resource(SingleFilmResource, "/films/<int:film_id>")

