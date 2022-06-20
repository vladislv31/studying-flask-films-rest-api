"""Restx directors models."""

from flask_restx import fields

from app import api

director_response = api.model("Director", {
    "id": fields.Integer(example=1),
    "first_name": fields.String(example="Sam"),
    "last_name": fields.String(example="Raimi")
})

directors_response = api.model("Directors Response", {
    "count": fields.Integer,
    "result": fields.List(fields.Nested(director_response))
})

directors_body = api.model("Directors Body", {
    "first_name": fields.String(example="Sam"),
    "last_name": fields.String(example="Raimi")
})

directors_add_response = api.model("Add Director Response", {
    "message": fields.String(example="Director has been created."),
    "result": fields.Nested(director_response)
})

directors_update_response = api.model("Update Director Response", {
    "message": fields.String(example="Director has been updated."),
    "result": fields.Nested(director_response)
})

directors_delete_response = api.model("Delete Director Response", {
    "message": fields.String(example="Director has been deleted.")
})
