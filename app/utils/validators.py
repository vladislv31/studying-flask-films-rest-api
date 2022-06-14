from app.utils.helpers import validate_date


def sort_by_validator(value):
    if value not in ["premiere_date", "rating"]:
        raise ValueError("Bad choice.")

    return value


def sort_order_validator(value):
    try:
        if int(value) not in [1, -1]:
            raise ValueError()

    except ValueError:
        raise ValueError("Incorrect order.")

    return value


def date_validator(value):
    if not validate_date(value):
        raise ValueError("Incorrect date.")

    return value


def rating_validator(value):
    try:
        if not (1 <= int(value) <= 10):
            raise ValueError()

    except ValueError:
        raise ValueError("Incorrect value.")

    return value


def genres_ids_validator(value):
    try:
        genres = value.split(",")
        for genre in genres:
            int(genre)

    except ValueError:
        raise ValueError("Incorrect format.")

    return value


def page_validator(value):
    try:
        if int(value) < 1:
            raise ValueError()

    except ValueError:
        raise ValueError("Incorrect page number.")

    return value


def genres_ids_list_validator(value):
    try:
        for id_ in value:
            int(id_)

    except ValueError:
        raise ValueError("Incorrect list of integers.")

    return value
