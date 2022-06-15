from faker import Faker

from app.database.models import Genre


faker_ = Faker()


def test_get_genres(client):
    resp = client.get("/films/")

    assert resp.status_code == 200
    assert set(resp.json.keys()) == {"count", "result"}


def test_add_genre(logged_admin):
    client = logged_admin

    added_genre_resp = client.post("/genres/", json={
        "name": "something"
    })

    assert added_genre_resp.status_code == 200

    added_genre = added_genre_resp.json
    added_genre_id = added_genre["result"]["id"]

    genre = Genre.query.filter_by(id=added_genre_id).first()

    assert genre
    assert genre.name == "something"


def test_add_genre_bad_request(logged_admin):
    client = logged_admin

    added_genre_resp = client.post("/genres/")

    assert added_genre_resp.status_code == 400


def test_add_genre_already_exists(logged_admin):
    client = logged_admin

    genres_resp = client.get("/genres/")
    genres = genres_resp.json
    exists_genre_name = genres["result"][0]["name"]

    added_genre_resp = client.post("/genres/", json={
        "name": exists_genre_name
    })

    assert added_genre_resp.status_code == 400


def test_add_genre_not_logged(not_logged_client):
    client = not_logged_client

    added_genre_resp = client.post("/genres/", json={
        "name": "something"
    })

    assert added_genre_resp.status_code == 401


def test_add_genre_not_admin(logged_client):
    client = logged_client

    added_genre_resp = client.post("/genres/", json={
        "name": "something"
    })

    assert added_genre_resp.status_code == 401


def test_update_genre(logged_admin):
    client = logged_admin

    added_genre_resp = client.post("/genres/", json={
        "name": "something_to_updated"
    })
    added_genre = added_genre_resp.json
    added_genre_id = added_genre["result"]["id"]

    added_genre = Genre.query.filter_by(id=added_genre_id).first()

    updated_genre_resp = client.put("/genres/{}".format(added_genre_id), json={
        "name": "something_else_to_updated"
    })
    updated_genre = updated_genre_resp.json
    updated_genre_id = updated_genre["result"]["id"]

    updated_genre = Genre.query.filter_by(id=updated_genre_id).first()

    assert updated_genre_resp.status_code == 200

    assert added_genre_id == updated_genre_id

    assert added_genre
    assert updated_genre

    assert updated_genre.name == "something_else_to_updated"


def test_update_genre_bad_request(logged_admin):
    client = logged_admin

    updated_genre_resp = client.put("/genres/1")

    assert updated_genre_resp.status_code == 400


def test_update_genre_not_found(logged_admin):
    client = logged_admin

    added_genre_resp = client.put("/genres/1000000", json={
        "name": "something"
    })

    assert added_genre_resp.status_code == 404


def test_update_genre_already_exists(logged_admin):
    client = logged_admin

    added_genre_resp = client.post("/genres/", json={
        "name": "something_else_to_update_with_exists_name"
    })
    added_genre = added_genre_resp.json
    added_genre_id = added_genre["result"]["id"]

    genres_resp = client.get("/genres/")
    genres = genres_resp.json
    exists_genre_name = genres["result"][0]["name"]

    updated_genre_resp = client.put("/genres/{}".format(added_genre_id), json={
        "name": exists_genre_name
    })

    assert updated_genre_resp.status_code == 400


def test_update_genre_not_logged(not_logged_client):
    client = not_logged_client

    added_genre_resp = client.put("/genres/1", json={
        "name": "something"
    })

    assert added_genre_resp.status_code == 401


def test_update_genre_not_admin(logged_client):
    client = logged_client

    added_genre_resp = client.put("/genres/1", json={
        "name": "something"
    })

    assert added_genre_resp.status_code == 401


def test_get_one_genre(logged_admin):
    client = logged_admin

    added_genre_resp = client.post("/genres/", json={
        "name": "something_to_get"
    })
    added_genre = added_genre_resp.json
    added_genre_id = added_genre["result"]["id"]

    one_genre_resp = client.get("/genres/{}".format(added_genre_id))
    one_genre = one_genre_resp.json

    assert one_genre_resp.status_code == 200
    assert one_genre["id"] == added_genre_id
    assert one_genre["name"] == "something_to_get"


def test_get_one_not_found(not_logged_client):
    client = not_logged_client

    one_genre_resp = client.get("/genres/10000")

    assert one_genre_resp.status_code == 404


def test_delete_genre(logged_admin):
    client = logged_admin

    added_genre_resp = client.post("/genres/", json={
        "name": "something_to_delete"
    })
    added_genre = added_genre_resp.json
    added_genre_id = added_genre["result"]["id"]

    delete_genre_resp = client.delete("/genres/{}".format(added_genre_id))

    deleted_genre = Genre.query.filter_by(id=added_genre_id).first()

    assert delete_genre_resp.status_code == 200
    assert not deleted_genre


def test_delete_genre_not_found(logged_admin):
    client = logged_admin

    added_genre_resp = client.delete("/genres/1000000")

    assert added_genre_resp.status_code == 404


def test_delete_genre_not_logged(not_logged_client):
    client = not_logged_client

    added_genre_resp = client.delete("/genres/1")

    assert added_genre_resp.status_code == 401


def test_delete_genre_not_admin(logged_client):
    client = logged_client

    added_genre_resp = client.delete("/genres/1")

    assert added_genre_resp.status_code == 401
