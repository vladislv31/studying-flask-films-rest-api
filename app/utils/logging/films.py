from app import app
from app.schemas.films import FilmSchema


def log_created_film(film: FilmSchema):
    log_msg = "Created film\n"
    log_msg += "\tID: %s\n"
    log_msg += "\tTitle: %s"

    app.logger.info(log_msg, film.id, film.title)


def log_updated_film(film: FilmSchema):
    log_msg = "Updated film\n"
    log_msg += "\tID: %s\n"
    log_msg += "\tTitle: %s"

    app.logger.info(log_msg, film.id, film.title)


def log_deleted_film(film_id: int):
    log_msg = "Deleted film\n"
    log_msg += "\tID: %s"

    app.logger.info(log_msg, film_id)
