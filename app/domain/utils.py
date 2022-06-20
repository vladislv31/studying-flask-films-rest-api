"""Module implements domain utils."""

from functools import wraps

from flask_login import current_user

from app.utils.exceptions import UnauthorizedError


def admin_required(func):
    """Checks for auth and if the user is admin."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin():
            raise UnauthorizedError()

        return func(*args, **kwargs)

    return wrapper
