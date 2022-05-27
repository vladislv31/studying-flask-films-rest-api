from flask_restful import reqparse


def film_args_parser():
    film_args_parser = reqparse.RequestParser()

    film_args_parser.add_argument("title", required=True, help="title cannot be blank!")
    film_args_parser.add_argument("premiere_date", required=True, help="premiere_date cannot be blank!")
    film_args_parser.add_argument("director_id", required=True, help="director_id cannot be blank!")
    film_args_parser.add_argument("description", required=True, help="description cannot be blank!")
    film_args_parser.add_argument("rating", required=True, help="rating cannot be blank!")
    film_args_parser.add_argument("poster_url", required=True, help="poster_url cannot be blank!")
    film_args_parser.add_argument("user_id", required=True, help="user_id cannot be blank!")

    return film_args_parser

