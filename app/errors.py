"""Module handling errors in routes."""

import traceback

from pydantic import ValidationError

from werkzeug.exceptions import NotFound

from flask import jsonify, request
from flask_login import current_user

from app import app
from app.utils.exceptions import UnauthorizedError


@app.errorhandler(NotFound)
def handle_not_found_error(_):
    return jsonify({"message": "Not found."}), 404


@app.errorhandler(UnauthorizedError)
def handle_unauthorized_error(_):
    app.logger.info(
        "%s tried %s %s with no access for it.",
        current_user.username,
        request.method,
        request.path
    )
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
def handle_unexpected_errors(_):
    app.logger.critical("There is a critical error. Look traceback below.")
    app.logger.critical(traceback.format_exc())

    return jsonify({"message": "Internal server error."}), 500
