import math
import random
from datetime import datetime

from app import app

from app.domain.films import get_all_films
from app.domain.directors import get_all_directors
from app.domain.genres import get_all_genres

from app.schemas.films import FilmsQuerySchema


def test_films_query_search(faker, films_crud):
    films = get_all_films(films_crud, FilmsQuerySchema.parse_obj({"page": -1}))

    for word in faker.words(app.config["EACH_TEST_REPEATS"]):
        searched_films = get_all_films(films_crud, FilmsQuerySchema.parse_obj({"search": word, "page": -1}))

        expected_films = []
        for film in films:
            if word.lower() in film.title.lower():
                expected_films.append(film)

        assert len(expected_films) == len(searched_films)
        assert set([str(film) for film in expected_films]) == set([str(film) for film in searched_films])


def test_films_query_director_filter(films_crud, directors_crud):
    films = get_all_films(films_crud, FilmsQuerySchema.parse_obj({"page": -1}))
    directors = get_all_directors(directors_crud)

    for director in directors:
        director_id = director.id
        filtered_films = get_all_films(films_crud, FilmsQuerySchema.parse_obj({"director_id": director_id, "page": -1}))

        expected_films = []
        for film in films:
            if film.director.id == director_id:
                expected_films.append(film)

        assert len(expected_films) == len(filtered_films)
        assert set([str(film) for film in expected_films]) == set([str(film) for film in filtered_films])


def test_films_query_sort_by_rating(films_crud):
    films = get_all_films(films_crud, FilmsQuerySchema.parse_obj({"page": -1}))

    films_ordered_asc = get_all_films(films_crud,
                                      FilmsQuerySchema.parse_obj({"sort_by": "rating", "sort_order": 1, "page": -1}))
    films_ordered_desc = get_all_films(films_crud,
                                       FilmsQuerySchema.parse_obj({"sort_by": "rating", "sort_order": -1, "page": -1}))

    expected_ordered_asc = sorted(films, key=lambda f: f.rating)
    expected_ordered_desc = sorted(films, key=lambda f: f.rating, reverse=True)

    assert expected_ordered_asc == films_ordered_asc
    assert expected_ordered_desc == films_ordered_desc


def test_films_query_sort_by_date(films_crud):
    films = get_all_films(films_crud, FilmsQuerySchema.parse_obj({"page": -1}))

    films_ordered_asc = get_all_films(films_crud,
                                      FilmsQuerySchema.parse_obj(
                                          {"sort_by": "premiere_date", "sort_order": 1, "page": -1}))
    films_ordered_desc = get_all_films(films_crud,
                                       FilmsQuerySchema.parse_obj(
                                           {"sort_by": "premiere_date", "sort_order": -1, "page": -1}))

    expected_ordered_asc = sorted(films, key=lambda f: f.premiere_date)
    expected_ordered_desc = sorted(films, key=lambda f: f.premiere_date, reverse=True)

    assert expected_ordered_asc == films_ordered_asc
    assert expected_ordered_desc == films_ordered_desc


def test_films_query_start_premiere_date(faker, films_crud):
    films = get_all_films(films_crud, FilmsQuerySchema.parse_obj({"page": -1}))

    for _ in range(app.config["EACH_TEST_REPEATS"]):
        date = faker.date_between_dates(date_start=datetime(2005, 1, 1), date_end=datetime(2022, 1, 1))
        date = str(date)

        filtered_films = get_all_films(films_crud,
                                       FilmsQuerySchema.parse_obj({"start_premiere_date": date, "page": -1}))

        expected_films = []
        for film in films:
            if datetime.strptime(str(film.premiere_date), "%Y-%m-%d") >= datetime.strptime(date, "%Y-%m-%d"):
                expected_films.append(film)

        assert len(expected_films) == len(filtered_films)
        assert set([str(film) for film in expected_films]) == set([str(film) for film in filtered_films])


def test_films_query_end_premiere_date(faker, films_crud):
    films = get_all_films(films_crud, FilmsQuerySchema.parse_obj({"page": -1}))

    for _ in range(app.config["EACH_TEST_REPEATS"]):
        date = faker.date_between_dates(date_start=datetime(2005, 1, 1), date_end=datetime(2022, 1, 1))
        date = str(date)

        filtered_films = get_all_films(films_crud,
                                       FilmsQuerySchema.parse_obj({"end_premiere_date": date, "page": -1}))

        expected_films = []
        for film in films:
            if datetime.strptime(str(film.premiere_date), "%Y-%m-%d") <= datetime.strptime(date, "%Y-%m-%d"):
                expected_films.append(film)

        assert len(expected_films) == len(filtered_films)
        assert set([str(film) for film in expected_films]) == set([str(film) for film in filtered_films])


def test_films_query_rating_filter(films_crud):
    films = get_all_films(films_crud, FilmsQuerySchema.parse_obj({"page": -1}))

    for rating in range(1, 11):
        filtered_films = get_all_films(films_crud, FilmsQuerySchema.parse_obj({"rating": rating, "page": -1}))

        expected_films = []
        for film in films:
            if film.rating == rating:
                expected_films.append(film)

        assert len(expected_films) == len(filtered_films)
        assert set([str(film) for film in expected_films]) == set([str(film) for film in filtered_films])


def test_films_query_genres_filter(films_crud, genres_crud):
    films = get_all_films(films_crud, FilmsQuerySchema.parse_obj({"page": -1}))
    genres = get_all_genres(genres_crud)

    for _ in range(app.config["EACH_TEST_REPEATS"]):
        genres_ids = []
        for _ in range(random.randrange(1, 4)):
            genre = random.choice(genres)
            genres_ids.append(str(genre.id))

        filtered_films = get_all_films(films_crud,
                                       FilmsQuerySchema.parse_obj({"genres_ids": ",".join(genres_ids), "page": -1}))

        expected_films = []
        for film in films:
            film_genres_ids = [str(genre.id) for genre in film.genres]
            if set(film_genres_ids) & set(genres_ids):
                expected_films.append(film)

        assert len(expected_films) == len(filtered_films)
        assert set([str(film) for film in expected_films]) == set([str(film) for film in filtered_films])


def test_films_query_page(films_crud):
    films_per_page = app.config["FILMS_PER_PAGE"]

    films_count = len(get_all_films(films_crud, FilmsQuerySchema.parse_obj({"page": -1})))

    if films_count >= films_per_page:
        assert len(get_all_films(films_crud, FilmsQuerySchema.parse_obj({"page": 1}))) == films_per_page
    else:
        assert len(get_all_films(films_crud, FilmsQuerySchema.parse_obj({"page": 1}))) == films_count

    last_page = math.ceil(films_count / films_per_page)

    if films_count % films_per_page == 0:
        last_page_count = films_per_page
    else:
        last_page_count = films_count % films_per_page

    assert len(get_all_films(films_crud, FilmsQuerySchema.parse_obj({"page": last_page}))) == last_page_count
    assert len(get_all_films(films_crud, FilmsQuerySchema.parse_obj({"page": last_page + 1}))) == 0
