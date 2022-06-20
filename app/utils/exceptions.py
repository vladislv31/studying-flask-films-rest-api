"""Exceptions that used in app."""


class EntityIdError(ValueError):
    pass


class DirectorIdError(EntityIdError):
    pass


class GenreIdError(EntityIdError):
    pass


class UnauthorizedError(Exception):
    pass


class GenreAlreadyExistsError(ValueError):
    pass

