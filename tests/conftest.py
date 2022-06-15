import pytest
import logging

from app import app
from app import db

from seeds import db_seed


def pytest_configure(config):
    app.logger.disabled = True

    app.config["TESTING"] = True
    app.config["EACH_TEST_REPEATS"] = 20
    app.testing = True

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with app.app_context():
        db.create_all()

    db_seed()


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def logged_client(client):
    client.post("/auth/login", json={
        "username": "just_a_user",
        "password": "123"
    })
    return client


@pytest.fixture
def logged_admin(client):
    client.post("/auth/login", json={
        "username": "admin",
        "password": "123"
    })
    return client


@pytest.fixture
def not_logged_client(client):
    client.post("/auth/logout")
    return client


@pytest.fixture
def films_data():
    return [
        {
            "title": "Added for testing film",
            "rating": 8,
            "premiere_date": "2022-06-18",
            "description": "Test film description.",
            "poster_url": "https://example.com/image.jpg"
        },
        {
            "title": "Added for testing film 2",
            "rating": 4,
            "premiere_date": "2015-06-18",
            "description": "Test film description.",
            "poster_url": "https://example.com/image.jpg"
        },
        {
            "title": "Added for testing film 3",
            "rating": 10,
            "premiere_date": "2013-02-14",
            "description": "Test film description.",
            "poster_url": "https://example.com/image.jpg"
        }
    ]


@pytest.fixture
def updated_film_data():
    return {
        "title": "Updated film data",
        "rating": 10,
        "premiere_date": "2022-2-2",
        "description": "Updated film description.",
        "poster_url": "https://example.com/updated.jpg"
    }
