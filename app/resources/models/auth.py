from flask_restx import fields

from app import api


user_response = api.model("Auth", {
    "username": fields.String(example="username")
})

login_response = api.model("Login", {
    "message": fields.String(example="Authentication done successfully.")
})

register_response = api.model("Register", {
    "message": fields.String(example="Registered successfully.")
})

logout_response = api.model("Logout", {
    "message": fields.String(example="Logout done successfully.")
})
