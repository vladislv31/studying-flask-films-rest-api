from faker import Faker

from app import app
from app.database.models import Director

from tests.e2e.utils import generate_director_data


faker_ = Faker()


def test_get_directors(client):
    resp = client.get("/directors/")

    assert resp.status_code == 200
    assert set(resp.json.keys()) == {"count", "result"}


def test_add_director(logged_admin):
    client = logged_admin

    for _ in range(app.config["EACH_TEST_REPEATS"]):
        director_data = generate_director_data()

        added_director_resp = client.post("/directors/", json={
            "first_name": director_data["first_name"],
            "last_name": director_data["last_name"]
        })

        assert added_director_resp.status_code == 200

        added_director = added_director_resp.json
        added_director_id = added_director["result"]["id"]

        director = Director.query.filter_by(id=added_director_id).first()

        assert director
        assert director.first_name == director_data["first_name"]
        assert director.last_name == director_data["last_name"]


def test_add_director_bad_request(logged_admin):
    client = logged_admin

    added_director_resp = client.post("/directors/")

    assert added_director_resp.status_code == 400


def test_add_director_bad_request_no_first_name(logged_admin):
    client = logged_admin

    added_director_resp = client.post("/directors/", json={
        "last_name": "Last Name"
    })

    assert added_director_resp.status_code == 400


def test_add_director_bad_request_no_last_name(logged_admin):
    client = logged_admin

    updated_director_resp = client.post("/directors/", json={
        "first_name": "First Name"
    })

    assert updated_director_resp.status_code == 400


def test_add_director_not_logged(not_logged_client):
    client = not_logged_client
    director_data = generate_director_data()

    added_director_resp = client.post("/directors/", json={
        "first_name": director_data["first_name"],
        "last_name": director_data["last_name"]
    })

    assert added_director_resp.status_code == 401


def test_add_director_not_admin(logged_client):
    client = logged_client
    director_data = generate_director_data()

    added_director_resp = client.post("/directors/", json={
        "first_name": director_data["first_name"],
        "last_name": director_data["last_name"]
    })

    assert added_director_resp.status_code == 401


def test_update_director(logged_admin):
    client = logged_admin

    for _ in range(app.config["EACH_TEST_REPEATS"]):
        added_director_data = generate_director_data()

        added_director_resp = client.post("/directors/", json={
            "first_name": added_director_data["first_name"],
            "last_name": added_director_data["last_name"]
        })
        added_director = added_director_resp.json
        added_director_id = added_director["result"]["id"]

        added_director = Director.query.filter_by(id=added_director_id).first()

        updated_director_data = generate_director_data()

        updated_director_resp = client.put("/directors/{}".format(added_director_id), json={
            "first_name": updated_director_data["first_name"],
            "last_name": updated_director_data["last_name"]
        })
        updated_director = updated_director_resp.json
        updated_director_id = updated_director["result"]["id"]

        updated_director = Director.query.filter_by(id=updated_director_id).first()

        assert updated_director_resp.status_code == 200

        assert added_director_id == updated_director_id

        assert added_director
        assert updated_director

        assert updated_director.first_name == updated_director_data["first_name"]
        assert updated_director.last_name == updated_director_data["last_name"]


def test_update_director_bad_request(logged_admin):
    client = logged_admin

    updated_director_resp = client.put("/directors/1")

    assert updated_director_resp.status_code == 400


def test_update_director_bad_request_no_first_name(logged_admin):
    client = logged_admin

    updated_director_resp = client.put("/directors/1", json={
        "last_name": "Last Name"
    })

    assert updated_director_resp.status_code == 400


def test_update_director_bad_request_no_last_name(logged_admin):
    client = logged_admin

    updated_director_resp = client.put("/directors/1", json={
        "first_name": "First Name"
    })

    assert updated_director_resp.status_code == 400


def test_update_director_not_found(logged_admin):
    client = logged_admin
    director_data = generate_director_data()

    added_director_resp = client.put("/directors/1000000", json={
        "first_name": director_data["first_name"],
        "last_name": director_data["last_name"]
    })

    assert added_director_resp.status_code == 404


def test_update_director_not_logged(not_logged_client):
    client = not_logged_client
    director_data = generate_director_data()

    added_director_resp = client.put("/directors/1000000", json={
        "first_name": director_data["first_name"],
        "last_name": director_data["last_name"]
    })

    assert added_director_resp.status_code == 401


def test_update_director_not_admin(logged_client):
    client = logged_client
    director_data = generate_director_data()

    added_director_resp = client.put("/directors/1000000", json={
        "first_name": director_data["first_name"],
        "last_name": director_data["last_name"]
    })

    assert added_director_resp.status_code == 401


def test_get_one_director(logged_admin):
    client = logged_admin

    for _ in range(app.config["EACH_TEST_REPEATS"]):
        director_data = generate_director_data()

        added_director_resp = client.post("/directors/", json={
            "first_name": director_data["first_name"],
            "last_name": director_data["last_name"]
        })
        added_director = added_director_resp.json
        added_director_id = added_director["result"]["id"]

        one_director_resp = client.get("/directors/{}".format(added_director_id))
        one_director = one_director_resp.json

        assert one_director_resp.status_code == 200
        assert one_director["id"] == added_director_id
        assert one_director["first_name"] == director_data["first_name"]
        assert one_director["last_name"] == director_data["last_name"]


def test_get_one_not_found(not_logged_client):
    client = not_logged_client

    one_director_resp = client.get("/directors/10000")

    assert one_director_resp.status_code == 404


def test_delete_director(logged_admin):
    client = logged_admin

    for _ in range(app.config["EACH_TEST_REPEATS"]):
        director_data = generate_director_data()

        added_director_resp = client.post("/directors/", json={
            "first_name": director_data["first_name"],
            "last_name": director_data["last_name"]
        })
        added_director = added_director_resp.json
        added_director_id = added_director["result"]["id"]

        delete_director_resp = client.delete("/directors/{}".format(added_director_id))

        deleted_director = Director.query.filter_by(id=added_director_id).first()

        assert delete_director_resp.status_code == 200
        assert not deleted_director


def test_delete_director_not_found(logged_admin):
    client = logged_admin

    added_director_resp = client.delete("/directors/1000000")

    assert added_director_resp.status_code == 404


def test_delete_director_not_logged(not_logged_client):
    client = not_logged_client

    added_director_resp = client.delete("/directors/1")

    assert added_director_resp.status_code == 401


def test_delete_director_not_admin(logged_client):
    client = logged_client

    added_director_resp = client.delete("/directors/1")

    assert added_director_resp.status_code == 401
