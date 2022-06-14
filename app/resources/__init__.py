from app import api

from app.resources.films import api as films_api
from app.resources.genres import api as genres_api
from app.resources.directors import api as directors_api

api.add_namespace(films_api)
api.add_namespace(genres_api)
api.add_namespace(directors_api)
