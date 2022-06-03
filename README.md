# Nix Flask Films Rest API

## How to run:

- clone repository
- poetry install
- poetry shell
- python wsgi.py

## .env file example:

```
SECRET_KEY=secret_key

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=123
DB_NAME=films_rest_api

APP_SETTINGS=app.config.DevelopmentConfig

SQLALCHEMY_DATABASE_URI=postgresql://postgres:123@localhost:5432/films_rest_api

FILMS_PER_PAGE=10
```
