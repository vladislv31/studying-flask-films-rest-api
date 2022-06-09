from flask_restx import reqparse

directors_body_parser = reqparse.RequestParser()

directors_body_parser.add_argument("first_name", required=True, type=str, help="Required string field.",
                                   location="json")
directors_body_parser.add_argument("last_name", required=True, type=str, help="Required string field.", location="json")
