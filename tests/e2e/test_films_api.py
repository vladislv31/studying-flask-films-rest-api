import random
from urllib.parse import urlencode
from datetime import datetime

import pytest

from tests.e2e.utils import generate_film_data

from app import app, db
from app.database.models import Film, User


def test_get_films(client):
    resp = client.get("/films/")

    assert resp.status_code == 200
    assert set(resp.json.keys()) == {"count", "result"}


def test_get_films_with_params(client, faker):
    directors_resp = client.get("/directors/")
    directors = directors_resp.json

    genres_resp = client.get("/genres/")
    genres = genres_resp.json

    for _ in range(app.config["EACH_TEST_REPEATS"]):
        search = faker.word()
        director_id = random.choice(directors["result"])["id"]
        start_premiere_date = faker.date_between_dates(date_start=datetime(2005, 1, 1), date_end=datetime(2022, 1, 1))
        end_premiere_date = faker.date_between_dates(date_start=start_premiere_date, date_end=datetime(2022, 1, 1))
        rating = random.randrange(1, 11)

        genres_ids = []
        for _ in range(random.randrange(1, 6)):
            genres_ids.append(random.choice([str(genre["id"]) for genre in genres["result"]]))

        page = 1
        while True:
            query_params = urlencode({
                "search": search,
                "director_id": director_id,
                "start_premiere_date": start_premiere_date,
                "end_premiere_date": end_premiere_date,
                "rating": rating,
                "genres_ids": ",".join(genres_ids),
                "page": page
            })
            films_resp = client.get("/films/?{}".format(query_params))
            films = films_resp.json

            if films["count"] == 0:
                break

            for film in films["result"]:
                assert search.lower() in film["title"].lower()
                assert film["director"]["id"] == director_id
                assert datetime.strptime(film["premiere_date"], "%Y-%m-%d") >= datetime.strptime(
                    str(start_premiere_date),
                    "%Y-%m-%d")
                assert datetime.strptime(film["premiere_date"], "%Y-%m-%d") <= datetime.strptime(str(end_premiere_date),
                                                                                                 "%Y-%m-%d")
                assert film["rating"] == rating
                assert set([str(genre["id"]) for genre in film["genres"]]) & set(genres_ids)

            page += 1


@pytest.mark.parametrize("params", [
    "director_id=something",
    "sort_by=something",
    "sort_order=2",
    "sort_order=0",
    "sort_order=-2",
    "sort_order=something",
    "start_premiere_date=something",
    "end_premiere_date=something",
    "rating=something",
    "rating=0",
    "rating=11",
    "genres_ids=asd",
    "genres_ids=a,b,c"
])
def test_get_films_with_bad_params(client, params):
    assert client.get("/films/?{}".format(params)).status_code == 400


def test_add_film(logged_client):
    client = logged_client

    for _ in range(app.config["EACH_TEST_REPEATS"]):
        film_data = generate_film_data(client)

        added_film_resp = client.post("/films/", json={
            "title": film_data["title"],
            "rating": film_data["rating"],
            "premiere_date": film_data["premiere_date"],
            "description": film_data["description"],
            "poster_url": film_data["poster_url"],
            "director_id": film_data["director_id"],
            "genres_ids": film_data["genres_ids"]
        })
        added_film = added_film_resp.json
        added_film_id = added_film["result"]["id"]

        film = Film.query.filter_by(id=added_film_id).first()

        assert film
        assert film.title == film_data["title"]
        assert film.rating == film_data["rating"]
        assert str(film.premiere_date) == film_data["premiere_date"]
        assert film.description == film_data["description"]
        assert film.poster_url == film_data["poster_url"]
        assert film.director_id == film_data["director_id"]
        assert set([genre.id for genre in film.genres]) == set(film_data["genres_ids"])


def test_add_film_not_logged(not_logged_client):
    client = not_logged_client

    film_data = generate_film_data(client)

    added_film_resp = client.post("/films/", json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })

    assert added_film_resp.status_code == 401


def test_add_film_no_title(logged_client):
    client = logged_client

    film_data = generate_film_data(client)

    added_film_resp = client.post("/films/", json={
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })

    assert added_film_resp.status_code == 400


def test_add_film_no_rating(logged_client):
    client = logged_client

    film_data = generate_film_data(client)

    added_film_resp = client.post("/films/", json={
        "title": film_data["title"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })

    assert added_film_resp.status_code == 400


@pytest.mark.parametrize("rating", [
    (11,),
    (0,),
    (-1,),
    (12,),
    (100,)
])
def test_add_film_bad_rating(rating, logged_client):
    client = logged_client

    film_data = generate_film_data(client)

    added_film_resp = client.post("/films/", json={
        "title": film_data["title"],
        "rating": rating,
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })

    assert added_film_resp.status_code == 400


def test_add_film_bad_premiere_date(logged_client):
    client = logged_client

    film_data = generate_film_data(client)

    added_film_resp = client.post("/films/", json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": "something",
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })

    assert added_film_resp.status_code == 400


@pytest.mark.parametrize("director_id", [
    (1000000,),
    ("something",)
])
def test_add_film_bad_director_id(director_id, logged_client):
    client = logged_client

    film_data = generate_film_data(client)

    added_film_resp = client.post("/films/", json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": director_id,
        "genres_ids": film_data["genres_ids"]
    })

    assert added_film_resp.status_code == 400


@pytest.mark.parametrize("genres_ids", [
    ["a", "b", "c"],
    ["something"],
    ["100", "200", "300"],
    [100, 200, 300],
])
def test_add_film_bad_genres_ids(genres_ids, logged_client):
    client = logged_client

    film_data = generate_film_data(client)

    added_film_resp = client.post("/films/", json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": genres_ids
    })

    assert added_film_resp.status_code == 400


def test_update_film(logged_client):
    client = logged_client

    for _ in range(app.config["EACH_TEST_REPEATS"]):
        film_data = generate_film_data(client)

        added_film_resp = client.post("/films/", json={
            "title": film_data["title"],
            "rating": film_data["rating"],
            "premiere_date": film_data["premiere_date"],
            "description": film_data["description"],
            "poster_url": film_data["poster_url"],
            "director_id": film_data["director_id"],
            "genres_ids": film_data["genres_ids"]
        })
        added_film_id = added_film_resp.json["result"]["id"]

        added_film = Film.query.filter_by(id=added_film_id).first()

        updated_film_data = generate_film_data(client)

        updated_film_resp = client.put("/films/{}".format(added_film_id), json={
            "title": updated_film_data["title"],
            "rating": updated_film_data["rating"],
            "premiere_date": updated_film_data["premiere_date"],
            "description": updated_film_data["description"],
            "poster_url": updated_film_data["poster_url"],
            "director_id": updated_film_data["director_id"],
            "genres_ids": updated_film_data["genres_ids"]
        })
        updated_film_id = updated_film_resp.json["result"]["id"]

        updated_film = Film.query.filter_by(id=updated_film_id).first()

        assert added_film_id == updated_film_id

        assert added_film
        assert updated_film

        assert added_film.id == updated_film.id
        assert updated_film_data["title"] == updated_film.title
        assert updated_film_data["rating"] == updated_film.rating
        assert updated_film_data["premiere_date"] == str(updated_film.premiere_date)
        assert updated_film_data["description"] == updated_film.description
        assert updated_film_data["poster_url"] == updated_film.poster_url
        assert updated_film_data["director_id"] == updated_film.director_id
        assert set(updated_film_data["genres_ids"]) == set([genre.id for genre in updated_film.genres])


def test_update_film_by_admin(logged_client):
    client = logged_client
    film_data = generate_film_data(client)

    added_film_resp = client.post("/films/", json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })
    added_film_id = added_film_resp.json["result"]["id"]

    client.post("/auth/login", json={
        "username": "admin",
        "password": "123"
    })

    updated_film_data = generate_film_data(client)

    updated_film_resp = client.put("/films/{}".format(added_film_id), json={
        "title": updated_film_data["title"],
        "rating": updated_film_data["rating"],
        "premiere_date": updated_film_data["premiere_date"],
        "description": updated_film_data["description"],
        "poster_url": updated_film_data["poster_url"],
        "director_id": updated_film_data["director_id"],
        "genres_ids": updated_film_data["genres_ids"]
    })

    assert updated_film_resp.status_code == 200


def test_update_film_not_logged(not_logged_client):
    client = not_logged_client

    film_data = generate_film_data(client)

    updated_film_resp = client.put("/films/1", json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })

    assert updated_film_resp.status_code == 401


def test_update_film_not_author(logged_client):
    client = logged_client
    added_film_data = generate_film_data(client)

    added_film_resp = client.post("/films/", json={
        "title": added_film_data["title"],
        "rating": added_film_data["rating"],
        "premiere_date": added_film_data["premiere_date"],
        "description": added_film_data["description"],
        "poster_url": added_film_data["poster_url"],
        "director_id": added_film_data["director_id"],
        "genres_ids": added_film_data["genres_ids"]
    })
    added_film = added_film_resp.json
    added_film_id = added_film["result"]["id"]

    client.post("/auth/register", json={
        "username": "another_user",
        "password": "123"
    })
    client.post("/auth/login", json={
        "username": "another_user",
        "password": "123"
    })

    updated_film_data = generate_film_data(client)

    updated_film_resp = client.put("/films/{}".format(added_film_id), json={
        "title": updated_film_data["title"],
        "rating": updated_film_data["rating"],
        "premiere_date": updated_film_data["premiere_date"],
        "description": updated_film_data["description"],
        "poster_url": updated_film_data["poster_url"],
        "director_id": updated_film_data["director_id"],
        "genres_ids": updated_film_data["genres_ids"]
    })

    assert updated_film_resp.status_code == 401

    User.query.filter_by(username="another_user").delete()
    db.session.commit()


def test_update_film_not_found(logged_client):
    client = logged_client

    film_data = generate_film_data(client)

    updated_film_resp = client.put("/films/10000", json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })

    assert updated_film_resp.status_code == 404


def test_update_film_no_title(logged_client):
    client = logged_client

    film_data = generate_film_data(client)

    added_film_resp = client.post("/films/", json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })
    added_film_id = added_film_resp.json["result"]["id"]

    updated_film_resp = client.put("/films/{}".format(added_film_id), json={
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })

    assert updated_film_resp.status_code == 400


def test_update_film_no_rating(logged_client):
    client = logged_client

    film_data = generate_film_data(client)

    added_film_resp = client.post("/films/", json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })
    added_film_id = added_film_resp.json["result"]["id"]

    updated_film_resp = client.put("/films/{}".format(added_film_id), json={
        "title": film_data["title"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })

    assert updated_film_resp.status_code == 400


@pytest.mark.parametrize("rating", [
    (11,),
    (0,),
    (-1,),
    (12,),
    (100,)
])
def test_update_film_bad_rating(rating, logged_client):
    client = logged_client

    film_data = generate_film_data(client)

    added_film_resp = client.post("/films/", json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })
    added_film_id = added_film_resp.json["result"]["id"]

    updated_film_resp = client.put("/films/{}".format(added_film_id), json={
        "title": film_data["title"],
        "rating": rating,
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })

    assert updated_film_resp.status_code == 400


def test_update_film_bad_premiere_date(logged_client):
    client = logged_client

    film_data = generate_film_data(client)

    added_film_resp = client.post("/films/", json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })
    added_film_id = added_film_resp.json["result"]["id"]

    updated_film_resp = client.put("/films/{}".format(added_film_id), json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": "something",
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })

    assert updated_film_resp.status_code == 400


@pytest.mark.parametrize("director_id", [
    (1000000,),
    ("something",)
])
def test_update_film_bad_director_id(director_id, logged_client):
    client = logged_client

    film_data = generate_film_data(client)

    added_film_resp = client.post("/films/", json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })
    added_film_id = added_film_resp.json["result"]["id"]

    updated_film_resp = client.put("/films/{}".format(added_film_id), json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": director_id,
        "genres_ids": film_data["genres_ids"]
    })

    assert updated_film_resp.status_code == 400


@pytest.mark.parametrize("genres_ids", [
    ["a", "b", "c"],
    ["something"],
    ["100", "200", "300"],
    [100, 200, 300],
])
def test_update_film_bad_genres_ids(genres_ids, logged_client):
    client = logged_client

    film_data = generate_film_data(client)

    added_film_resp = client.post("/films/", json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })
    added_film_id = added_film_resp.json["result"]["id"]

    updated_film_resp = client.put("/films/{}".format(added_film_id), json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": genres_ids
    })

    assert updated_film_resp.status_code == 400


def test_get_one_film(logged_client):
    client = logged_client

    for _ in range(app.config["EACH_TEST_REPEATS"]):
        film_data = generate_film_data(client)

        added_film_resp = client.post("/films/", json={
            "title": film_data["title"],
            "rating": film_data["rating"],
            "premiere_date": film_data["premiere_date"],
            "description": film_data["description"],
            "poster_url": film_data["poster_url"],
            "director_id": film_data["director_id"],
            "genres_ids": film_data["genres_ids"]
        })
        added_film = added_film_resp.json
        added_film_id = added_film["result"]["id"]

        one_film_resp = client.get("/films/{}".format(added_film_id))
        film_from_api = one_film_resp.json

        film_from_db = Film.query.filter_by(id=added_film_id).first()

        assert film_from_db
        assert film_from_db.title == film_from_api["title"]
        assert film_from_db.rating == film_from_api["rating"]
        assert str(film_from_db.premiere_date) == film_from_api["premiere_date"]
        assert film_from_db.description == film_from_api["description"]
        assert film_from_db.poster_url == film_from_api["poster_url"]
        assert film_from_db.director.id == film_from_api["director"]["id"]
        assert set([genre.id for genre in film_from_db.genres]) == set(
            [genre["id"] for genre in film_from_api["genres"]])


def test_get_one_film_not_found(logged_client):
    client = logged_client

    one_film_resp = client.get("/films/100000")

    assert one_film_resp.status_code == 404


def test_delete_film(logged_client):
    client = logged_client

    for _ in range(app.config["EACH_TEST_REPEATS"]):
        film_data = generate_film_data(client)

        added_film_resp = client.post("/films/", json={
            "title": film_data["title"],
            "rating": film_data["rating"],
            "premiere_date": film_data["premiere_date"],
            "description": film_data["description"],
            "poster_url": film_data["poster_url"],
            "director_id": film_data["director_id"],
            "genres_ids": film_data["genres_ids"]
        })
        added_film = added_film_resp.json
        added_film_id = added_film["result"]["id"]

        deleted_film_resp = client.delete("/films/{}".format(added_film_id))
        assert deleted_film_resp.status_code == 200
        assert deleted_film_resp.json["message"] == "Film has been deleted."

        deleted_film = Film.query.filter_by(id=added_film_id).first()
        assert not deleted_film


def test_delete_film_by_admin(logged_client):
    client = logged_client
    film_data = generate_film_data(client)

    added_film_resp = client.post("/films/", json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })
    added_film_id = added_film_resp.json["result"]["id"]

    client.post("/auth/login", json={
        "username": "admin",
        "password": "123"
    })

    deleted_film_resp = client.delete("/films/{}".format(added_film_id))

    assert deleted_film_resp.status_code == 200


def test_delete_film_not_logged(not_logged_client):
    client = not_logged_client

    deleted_film_resp = client.delete("/films/1")

    assert deleted_film_resp.status_code == 401


def test_delete_film_not_author(logged_client):
    client = logged_client
    film_data = generate_film_data(client)

    added_film_resp = client.post("/films/", json={
        "title": film_data["title"],
        "rating": film_data["rating"],
        "premiere_date": film_data["premiere_date"],
        "description": film_data["description"],
        "poster_url": film_data["poster_url"],
        "director_id": film_data["director_id"],
        "genres_ids": film_data["genres_ids"]
    })
    added_film = added_film_resp.json
    added_film_id = added_film["result"]["id"]

    client.post("/auth/register", json={
        "username": "another_user",
        "password": "123"
    })
    client.post("/auth/login", json={
        "username": "another_user",
        "password": "123"
    })

    deleted_film_resp = client.delete("/films/{}".format(added_film_id))

    assert deleted_film_resp.status_code == 401

    User.query.filter_by(username="another_user").delete()
    db.session.commit()


def test_delete_film_not_found(logged_client):
    client = logged_client

    deleted_film_resp = client.delete("/films/100000")

    assert deleted_film_resp.status_code == 404
