from flask_restx import fields

from app import api


role = api.model("Role", {
    "id": fields.Integer(example=1),
    "name": fields.String(example="user")
})

user = api.model("User", {
    "id": fields.Integer(example=1),
    "username": fields.String(example="administrator")
})

user_info = api.inherit("User Info", user, {
    "role": fields.Nested(role)
})
