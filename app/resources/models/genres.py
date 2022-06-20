"""Restx genres models."""

from flask_restx import fields

from app import api

genre_response = api.model("Genre", {
    "id": fields.Integer(example=1),
    "name": fields.String(example="Comedy")
})

genres_response = api.model("Genres Response", {
    "count": fields.Integer,
    "result": fields.List(fields.Nested(genre_response))
})

genres_body = api.model("Genres Body", {
    "name": fields.String(example="Comedy")
})

genres_add_response = api.model("Add Genre Response", {
    "message": fields.String(example="Genre has been created."),
    "result": fields.Nested(genre_response)
})

genres_update_response = api.model("Update Genre Response", {
    "message": fields.String(example="Genre has been updated."),
    "result": fields.Nested(genre_response)
})

genres_delete_response = api.model("Delete Genre Response", {
    "message": fields.String(example="Genre has been deleted.")
})
