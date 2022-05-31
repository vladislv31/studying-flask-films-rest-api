from datetime import date

from flask_login import UserMixin

from app import db
from app.exceptions import TitleValueError, PremiereDateValueError, RatingValueError
from app.utils.helpers import validate_date

from sqlalchemy.orm import validates


class Role(db.Model):

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)

    def __repr__(self):
        return f"<Role name={self.name}>"


class User(db.Model, UserMixin):
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return f"<User username={self.username}, role_id={self.role_id}>"


class Director(db.Model):

    __tablename__ = "directors"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Director first_name={self.first_name}, last_name={self.last_name}>"

    
film_genres = db.Table("film_genres",
    db.Column("film_id", db.Integer, db.ForeignKey("films.id", ondelete="CASCADE")),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id", ondelete="CASCADE"))
)


class Genre(db.Model):

    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"<Genre name={self.genre}>"


class Film(db.Model):

    __tablename__ = "films"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    premiere_date = db.Column(db.Date)
    description = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    genres = db.relationship("Genre", secondary=film_genres)

    director_id = db.Column(db.Integer, db.ForeignKey("directors.id", ondelete="SET NULL"), nullable=True)
    director = db.relationship("Director")

    def __repr__(self):
        return f"<Film title={self.title}, premiere_date={self.premiere_date}>"

