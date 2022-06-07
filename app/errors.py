import traceback

from flask import jsonify

from pydantic import ValidationError

from app import app
from app.utils.exceptions import UnauthorizedError


@app.errorhandler(UnauthorizedError)
def handle_unauthorized_error(err):
    return jsonify({"message": "Access denied."}), 401


@app.errorhandler(ValidationError)
def handle_validation_error(err):
    validation_errors = err.errors()

    field_name = validation_errors[0]["loc"][0]
    error_message = validation_errors[0]["msg"]

    return jsonify(
        {
            "message": "{} {}.".format(field_name, error_message)
        }
    ), 400


@app.errorhandler(Exception)
def handle_unexpected_errors(ex):
    traceback.print_exc()  # logging in future
    return jsonify({"message": "Internal server error."}), 500
