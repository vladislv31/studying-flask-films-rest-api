from app import app
from app.schemas.genres import GenreSchema


def log_created_genre(genre: GenreSchema):
    log_msg = "Created genre\n"
    log_msg += "\tID: %s\n"
    log_msg += "\tName: %s"

    app.logger.info(log_msg, genre.id, genre.name)


def log_updated_genre(genre: GenreSchema):
    log_msg = "Updated genre\n"
    log_msg += "\tID: %s\n"
    log_msg += "\tName: %s"

    app.logger.info(log_msg, genre.id, genre.name)


def log_deleted_genre(genre_id: int):
    log_msg = "Deleted genre\n"
    log_msg += "\tID: %s"

    app.logger.info(log_msg, genre_id)
