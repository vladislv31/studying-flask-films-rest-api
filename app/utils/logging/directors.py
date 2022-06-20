"""Logging utils for directors."""

from app import app
from app.schemas.directors import DirectorSchema


def log_created_director(director: DirectorSchema):
    log_msg = "Created director\n"
    log_msg += "\tID: %s\n"
    log_msg += "\tFirst name: %s\n"
    log_msg += "\tLast name: %s"

    app.logger.info(log_msg, director.id, director.first_name, director.last_name)


def log_updated_director(director: DirectorSchema):
    log_msg = "Updated director\n"
    log_msg += "\tID: %s\n"
    log_msg += "\tFirst name: %s\n"
    log_msg += "\tLast name: %s"

    app.logger.info(log_msg, director.id, director.first_name, director.last_name)


def log_deleted_director(director_id: int):
    log_msg = "Deleted director\n"
    log_msg += "\tID: %s"

    app.logger.info(log_msg, director_id)
