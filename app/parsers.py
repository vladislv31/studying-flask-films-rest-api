"""Module with implemented Restful reqeusts paresers and data types."""

from flask_restful import reqparse
from app.utils.helpers import validate_date


# parser args types

def data_allowed(type_, allowed):
    """Validates value checking for being it in allowed values list."""

    def validate(value):
        if type_(value) in allowed:
            return type_(value)
        raise ValueError

    return validate

def date_field():
    """Validates date."""

    def validate(value):
        if validate_date(value):
            return value
        raise ValueError

    return validate

def not_nullable():
    """Validates value checking it for nullable."""

    def validate(value):
        if value is not None:
            return value
        raise ValueError

    return validate

def range_type(start, end):
    """Validates int for being in range."""

    def validate(value):
        if start <= int(value) <= end:
            return value
        raise ValueError

    return validate

def array_type(delimiter):
    """Validates value and splitting it by delimiter."""

    def validate(value):
        array = value.split(delimiter)
        return array

    return validate


# parsers

def film_body_parser():
    """Returns body film parser.
    Checking fields:
        - title             required string field
        - premiere_date     not required string field in format YYY-m-d
        - director_id       not required int field
        - description       not required string field
        - rating            required int field in range 0-10
        - poster_url        not required string field
        - user_id           required int field
        - genres_id         not required string field in format genre_1,genre_2,genre_3
    """
    film_body_req_parser = reqparse.RequestParser()

    film_body_req_parser.add_argument("title",
            required=True,
            nullable=False,
            help="title is required field.",
            type=not_nullable(),
            location="json")

    film_body_req_parser.add_argument("premiere_date",
            required=False,
            help="premiere_date should be specified in format YYYY-m-d.",
            type=date_field(),
            location="json")

    film_body_req_parser.add_argument("director_id",
            required=False,
            help="director_id should be specified as integer.",
            type=int,
            location="json")

    film_body_req_parser.add_argument("description",
            required=False,
            help="description cannot be blank.",
            location="json")

    film_body_req_parser.add_argument("rating",
            required=True,
            help="rating is required field with integer type.",
            type=range_type(0, 10),
            location="json")

    film_body_req_parser.add_argument("poster_url",
            required=False,
            help="poster_url cannot be blank!",
            location="json")

    film_body_req_parser.add_argument("genres_ids",
            required=False,
            help="genres_ids should be specified in format genre_1,genre_2,genre_3.",
            type=array_type(","),
            location="json")

    return film_body_req_parser


def film_args_parser():
    """Returns query parameters film parser.
    Checking fields:
        - search                    not required string field
        - sort_order                not required int field: -1, 1
        - sort_by                   not required string field: rating, premiere_date
        - director_id               not required int field
        - start_premiere_date       not required string field in format YYYY-m-d
        - end_premiere_date         not required string field in format YYYY-m-d
        - genres_id                 not required string field in format genre_1,genre_2,genre_3
    """
    film_args_req_parser = reqparse.RequestParser()

    film_args_req_parser.add_argument("search", required=False, location="args")

    film_args_req_parser.add_argument("sort_order",
            required=False,
            help="sort_order allowed values: -1, 1.",
            type=data_allowed(int, [-1, 1]),
            location="args")

    film_args_req_parser.add_argument("sort_by",
            required=False,
            help="sort_by allowed values: rating, premiere_date.",
            type=data_allowed(str, ["rating", "premiere_date"]),
            location="args")

    film_args_req_parser.add_argument("director_id",
            required=False,
            help="director_id should be specified like integer.",
            type=int,
            location="args")

    film_args_req_parser.add_argument("start_premiere_date",
            required=False,
            help="start_premiere_date should be specified in format YYYY-m-d.",
            type=date_field(),
            location="args")

    film_args_req_parser.add_argument("end_premiere_date",
            required=False,
            help="end_premiere_date should be specified in format YYYY-m-d.",
            type=date_field(),
            location="args")

    film_args_req_parser.add_argument("genres_ids",
            required=False,
            help="genres_ids should be specified in format genre_1,genre_2,genre_3.",
            type=array_type(","),
            location="args")

    return film_args_req_parser

