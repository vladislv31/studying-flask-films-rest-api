from app.models import Film, Director


def get_all_films():
    films_query = Film.query.join(Director, Film.director_id == Director.id). \
        add_columns(
            Film.id,
            Film.title,
            Film.premiere_date,
            Director.first_name.label("director_first_name"),
            Director.last_name.label("director_last_name"),
            Film.description,
            Film.rating,
            Film.poster_url,
            Film.user_id
        )


    films = []

    for film in films_query:
        films.append({
            "id": film.id,
            "title": film.title,
            "premiere_date": str(film.premiere_date),
            "director": f"{film.director_first_name} {film.director_last_name}",
            "description": film.description,
            "rating": film.rating,
            "poster_url": film.poster_url,
            "user_id": film.user_id
        })

    return films

