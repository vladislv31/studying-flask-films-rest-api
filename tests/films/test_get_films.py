import pytest

from app import app


def test_simple_requests():
    requests_urls = [
        "/films",
        "/films?search=something",
        "/films?director_id=1",
        "/films?genres_ids=1,2",
        "/films?start_premiere_date=2010-2-2",
        "/films?end_premiere_date=2020-2-2",
        "/films?start_premiere_date=2010-2-2&end_premiere_date=2020-2-2",
        "/films?sort_order=1",
        "/films?sort_order=-1",
        "/films?sort_by=rating",
        "/films?sort_by=premiere_date",
        "/films?sort_order=1&sort_by=rating",
        "/films?sort_order=-1&sort_by=premiere_date",
    ]

    with app.test_client() as client:
        for url in requests_urls:
            response = client.get(url)
            result = response.json

            assert response.status_code == 200
            assert list(result.keys()) == ["count", "result"]


def test_bad_requests():
    requests_urls = [
        ("director_id", "/films?director_id=something"),
        ("start_premiere_date", "/films?start_premiere_date=something"),
        ("end_premiere_date", "/films?end_premiere_date=something"),
        ("sort_order", "/films?sort_order=something"),
        ("sort_by", "/films?sort_by=something"),
    ]

    with app.test_client() as client:
        for bad_field, url in requests_urls:
            response = client.get(url)
            result = response.json

            assert response.status_code == 400
            assert "message" in list(result.keys())
            assert bad_field in list(result["message"].keys())


def test_bad_requests_messages():
    requests_urls = [
        (
            "director_id should be specified like integer.",
            "/films?director_id=something"
        ),
        (
            "start_premiere_date should be specified in format YYYY-m-d.",
            "/films?start_premiere_date=something"
        ),
        (
            "end_premiere_date should be specified in format YYYY-m-d.",
            "/films?end_premiere_date=something"
        ),
        (
            "sort_order allowed values: -1, 1.",
            "/films?sort_order=something"
        ),
        (
            "sort_by allowed values: rating, premiere_date.",
            "/films?sort_by=something"
        )
    ]

    with app.test_client() as client:
        for message, url in requests_urls:
            response = client.get(url)
            result = response.json

            assert message == list(result["message"].values())[0]

