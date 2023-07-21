from flask import render_template, Blueprint

from .models.movie import Movie

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/index')
def index():
    return render_template('index.html')


@views.route('/blog')
def blog():
    public_movies = (
        Movie.query
        .filter_by(is_public=True)
        .order_by(Movie.post_date.desc())
        .all()
    )
    return render_template('records.html', chosen='Public', movies=public_movies)


@views.route('/ratings')
def ratings():
    rating_movies = Movie.query.filter_by(is_public=True).all()
    for rating_movie in rating_movies:
        rating_movie.sum_likes = sum([like.value for like in rating_movie.likes])
    sorted_rating_movies = sorted(rating_movies, key=lambda movie: movie.sum_likes, reverse=True)
    return render_template('records.html', chosen='Ratings', movies=sorted_rating_movies)
