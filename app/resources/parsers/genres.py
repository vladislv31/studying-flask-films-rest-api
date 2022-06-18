"""Restx genres parsers."""

from flask_restx import reqparse

genres_body_parser = reqparse.RequestParser()

genres_body_parser.add_argument("name", required=True, type=str, help="Required string field.", location="json")
