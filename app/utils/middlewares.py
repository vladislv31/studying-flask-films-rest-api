import json

from werkzeug.wrappers import Response

from app.utils.responses import internal_server_response_message
from app.utils.exceptions import UnauthorizedError


def create_response(body, status_code):
    response = Response(
            json.dumps(body),
            mimetype="text/json",
            status=status_code
    )

    return response


class UnexceptedErrorsMiddleware:
    """Returns unexcepted errors like internal server error."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        response = None

        try:
            return self.app(environ, start_response)

        except UnauthorizedError as err:
            response = create_response({"message": "Access denied."}, 401)

        except Exception as ex:
            print(ex) # logging in future
            response = create_response(internal_server_response_message()[0], 500)

        return response(environ, start_response)
