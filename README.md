# Nix Flask Films Rest API

## Basic

### How to run:

- clone repository
- poetry install
- poetry shell
- python wsgi.py

### .env file example:

```
SECRET_KEY=secret_key
APP_SETTINGS=app.config.DevelopmentConfig
SQLALCHEMY_DATABASE_URI=postgresql://postgres:123@db:5432/films_rest_api
FILMS_PER_PAGE=10
ADMIN_PASSWORD=123
```
## Docker

### First run:

- poetry install
- make build
- make start
- make init_db

### Remove containers:

- make remove

### Tests:

- make test_app

### Seeds:

- make seed_db

### Logs:

- make logs

### DB commands:

- make migrate_db
- make upgrade_db

### For clear database:

- make stop
- sudo rm -rf ./pg_data
- sudo docker-compose up -d --no-deps --build db
- make start
- make init_db