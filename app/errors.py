import traceback

from flask import jsonify

from app import app
from app.utils.exceptions import UnauthorizedError


@app.errorhandler(UnauthorizedError)
def handle_unauthorized_error(err):
    return jsonify({"message": "Access denied."}), 401


@app.errorhandler(Exception)
def handle_unexpected_errors(ex):
    traceback.print_exc()  # logging in future
    return jsonify({"message": "Internal server error."}), 500
