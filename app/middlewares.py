import json

from werkzeug.wrappers import Response

from app.utils.responses import internal_server_response_message


class InternalErrorMiddleware:
    """Returns unexcepted errors like internal server error."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)

        except Exception as ex:
            print(ex) # logging in future
            response = Response(
                    json.dumps(internal_server_response_message()[0]),
                    mimetype="text/json",
                    status=500
            )
            return response(environ, start_response)

