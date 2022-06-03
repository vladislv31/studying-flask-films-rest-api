from app.database.models import Film, Genre


def films_search_filter(query: Film.query, search: str) -> Film.query:
    if search:
        search_like = "%{}%".format(search)
        query = query.filter(Film.title.like(search_like))

    return query


def films_director_filter(query, director_id):
    if director_id:
        query = query.filter(Film.director_id == director_id)

    return query


def films_premiere_date_filter(query, start_premiere_date, end_premiere_date):
    if start_premiere_date:
        query = query.filter(Film.premiere_date >= start_premiere_date)

    if end_premiere_date:
        query = query.filter(Film.premiere_date <= end_premiere_date)

    return query


def films_genres_ids_filter(query, genres_ids):
    if genres_ids:
        query = query.filter(Film.genres.any(Genre.id.in_(genres_ids.split(","))))

    return query


def films_ordering_sorting(query, sort_by, sort_order):
    order_field = Film.id

    if sort_by == "rating":
        order_field = Film.rating
    elif sort_by == "premiere_date":
        order_field = Film.premiere_date

    order_by = order_field.asc()

    if sort_order == -1:
        order_by = order_field.desc()

    return query.order_by(order_by)

