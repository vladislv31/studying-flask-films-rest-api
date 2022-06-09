from flask_restx import fields

from app import api
from app.resources.models.directors import director_response
from app.resources.models.users import user
from app.resources.models.genres import genre_response


film_response = api.model("Film", {
    "id": fields.Integer(example=1),
    "title": fields.String(example="Film title"),
    "premiere_date": fields.String(example="2010-04-29"),
    "description": fields.String(example="Film description."),
    "rating": fields.Integer(example=10),
    "poster_url": fields.String(example="Image link."),
    "director": fields.Nested(director_response),
    "user": fields.Nested(user),
    "genres": fields.List(fields.Nested(genre_response))
})

films_response = api.model("Films Response", {
    "count": fields.Integer,
    "result": fields.List(fields.Nested(film_response))
})

films_body = api.model("Films Request", {
    "title": fields.String(example="Film title"),
    "rating": fields.Integer(example=10),
    "premiere_date": fields.String(example="2022-2-2"),
    "description": fields.String(example="Film description"),
    "poster_url": fields.String(example="https://example.com/image.jpg"),
    "director_id": fields.Integer(example=1),
    "genres_ids": fields.List(fields.Integer, example=[1, 2, 3])
})

films_add_response = api.model("Add Film Response", {
    "message": fields.String(example="Film has been created."),
    "result": fields.Nested(film_response)
})

films_update_response = api.model("Update Film Response", {
    "message": fields.String(example="Film has been updated."),
    "result": fields.Nested(film_response)
})

films_delete_response = api.model("Delete Film Response", {
    "message": fields.String(example="Film has been deleted.")
})
