from flask import render_template, Blueprint
from flask_login import login_required, current_user

from .models.movie import Movie
from .models.tag import Tag

categories = Blueprint('categories', __name__)


@categories.route('/watched')
@login_required
def watched():
    watched_movies = (
        Movie.query
        .join(Movie.tags)
        .filter(Movie.user == current_user, Tag.name == 'watched')
        .order_by(Movie.post_date.desc())
        .all()
    )
    return render_template('records.html', chosen='Watched', movies=watched_movies)


@categories.route('/towatch')
@login_required
def to_watch():
    to_watch_movies = (
        Movie.query
        .join(Movie.tags)
        .filter(Movie.user == current_user, Tag.name == 'towatch')
        .order_by(Movie.post_date.desc())
        .all()
    )
    return render_template('records.html', chosen='To Watch', movies=to_watch_movies)


@categories.route('/favorite')
@login_required
def favorite():
    favorite_movies = (
        Movie.query
        .join(Movie.tags)
        .filter(Movie.user == current_user, Tag.name == 'favorite')
        .order_by(Movie.post_date.desc())
        .all()
    )
    return render_template('records.html', chosen='Favorite', movies=favorite_movies)


@categories.route('/public')
@login_required
def public():
    public_movies = (
        Movie.query
        .filter_by(is_public=True)
        .order_by(Movie.post_date.desc())
        .all()
    )
    return render_template('records.html', chosen='Public', movies=public_movies)
