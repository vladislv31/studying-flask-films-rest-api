from flask_login import current_user

from app.models import Film
from app.utils.responses import not_found_request_response_message, \
    unauthorized_request_response_message


def single_film_middleware(resource):
    def wrapper(*args, **kwargs):
        film_id = kwargs["film_id"]
        
        film = Film.query.filter_by(id=film_id).first()

        if not film:
            return not_found_request_response_message("Film with such id not found.")
        
        if film.user_id != current_user.id and not current_user.is_admin():
            return unauthorized_request_response_message()

        return resource(*args, **kwargs)

    return wrapper

