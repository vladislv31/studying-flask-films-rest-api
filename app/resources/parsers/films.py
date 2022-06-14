from flask_restx import reqparse

from app.utils.validators import sort_by_validator, sort_order_validator, date_validator, rating_validator, \
    genres_ids_validator, genres_ids_list_validator, page_validator


films_query_parser = reqparse.RequestParser()

films_query_parser.add_argument("search", type=str, location="args")
films_query_parser.add_argument("director_id", type=int, help="Should be specified as integer.", location="args")
films_query_parser.add_argument("sort_by", type=sort_by_validator, help="Allowed values: premiere_date, rating.",
                                location="args")
films_query_parser.add_argument("sort_order", type=sort_order_validator, help="Allowed values: 1, -1.", location="args")
films_query_parser.add_argument("start_premiere_date", type=date_validator, help="Should be specified in format: "
                                                                                 "YYYY-m-d.",
                                location="args")
films_query_parser.add_argument("end_premiere_date", type=date_validator, help="Should be specified in format: "
                                                                               "YYYY-m-d.",
                                location="args")
films_query_parser.add_argument("rating", type=rating_validator, help="Integer in range [1, 10].", location="args")
films_query_parser.add_argument("genres_ids", type=genres_ids_validator, help="IDs in format: 1,2,3.", location="args")
films_query_parser.add_argument("page", type=page_validator, help="Integer more than 0.", location="args")

films_body_parser = reqparse.RequestParser()
films_body_parser.add_argument("title", required=True, type=str, help="Required string field.", location="json")
films_body_parser.add_argument("director_id", type=int, help="Should be specified as integer.", location="json")
films_body_parser.add_argument("description", type=str, help="Text field.", location="json")
films_body_parser.add_argument("premiere_date", type=date_validator, help="Should be specified in format: YYYY-m-d.",
                               location="json")
films_body_parser.add_argument("rating", required=True, help="Integer in range [1, 10].", type=rating_validator,
                               location="json")
films_body_parser.add_argument("poster_url", type=str, help="String field.", location="json")
films_body_parser.add_argument("genres_ids", type=genres_ids_list_validator, help="List of IDs.", location="json")
