import sqlalchemy.exc
from flask import render_template, Blueprint, redirect, url_for, request, flash
from flask_login import login_required, current_user
from sqlalchemy.exc import NoResultFound
from werkzeug.utils import secure_filename
from os import path

from . import db
from .models.movie import Movie
from .models.user import User
from .models.like import Like
from .models.genre import Genre
from .models.tag import Tag
from .models.author import Author
from .models.actor import Actor

movies = Blueprint('movies', __name__)


@movies.route('/<title>')
@login_required
def private_movie(title):
    try:
        movie = Movie.query.filter_by(user=current_user, title=title).one()
    except NoResultFound:
        return redirect(url_for('categories.watched'))
    likes = None
    if movie.is_public:
        likes = sum([like.value for like in movie.likes])
    return render_template('movie.html', chosen='Movie', movie=movie, likes=likes)


@movies.route('/<nickname>/<title>')
@login_required
def public_movie(nickname, title):
    try:
        user = User.query.filter_by(nickname=nickname).one()
        movie = Movie.query.filter_by(user=user, title=title, is_public=True).one()
    except NoResultFound:
        return redirect(url_for('categories.public'))
    likes = sum([like.value for like in movie.likes])
    liked1 = True if (
        Like.query
            .filter_by(user=current_user, value=1)
            .join(Movie)
            .filter_by(title=title)
            .join(User)
            .filter_by(nickname=nickname)
            .with_entities(Like)
            .first()
    ) else False
    liked2 = True if (
        Like.query
            .filter_by(user=current_user, value=2)
            .join(Movie)
            .filter_by(title=title)
            .join(User)
            .filter_by(nickname=nickname)
            .with_entities(Like)
            .first()
    ) else False
    return render_template('movie.html', chosen='Movie', movie=movie, likes=likes, liked1=liked1, liked2=liked2)


@movies.post('/<nickname>/<title>')
@login_required
def like_public_movie(nickname, title):
    liked1 = request.form.get('like1')
    liked2 = request.form.get('like2')
    value = 1 if liked1 is not None else 0
    value += 2 if liked2 is not None else 0
    users_like_on_movie = (
        Like.query
            .filter_by(user=current_user, value=value)
            .join(Movie)
            .filter_by(title=title)
            .join(User)
            .filter_by(nickname=nickname)
            .with_entities(Like)
            .first()
    )
    if users_like_on_movie:
        db.session.delete(users_like_on_movie)
        db.session.commit()
    else:
        movie_id = (
            Movie.query
                .filter_by(title=title)
                .join(User)
                .filter_by(nickname=nickname)
                .with_entities(Movie.id)
                .first()
        ).id
        new_like = Like(value=value, userid=current_user.id, movieid=movie_id)
        db.session.add(new_like)
        db.session.commit()

    return redirect(url_for('movies.public_movie', nickname=nickname, title=title))


@movies.post('/<nickname>/<title>/delete')
def delete(nickname, title):
    if nickname != current_user.nickname:
        return redirect(url_for('movies.public_movie', nickname=nickname, title=title))
    movie = (
        Movie.query
            .filter_by(title=title)
            .join(User)
            .filter_by(nickname=nickname)
            .with_entities(Movie)
            .first()
    )
    if not movie:
        return redirect(url_for('movies.public_movie', nickname=nickname, title=title))

    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('categories.watched'))


@movies.route('/new')
@login_required
def new():
    genres = [genre.name for genre in Genre.query.all()]
    tags = [tag.name for tag in Tag.query.all()]
    prev_data = {arg: value for arg, value in request.args.items() if arg != 'checked_tags'}
    checked_tags = request.args.getlist('checked_tags') if 'checked_tags' in request.args.keys() else []
    return render_template('new.html', chosen='New Movie', genres=genres, tags=tags,
                           **prev_data, checked_tags=checked_tags)


@movies.post('/new')
@login_required
def save_new_movie():
    title = request.form.get('title')
    premiere = request.form.get('premiere')
    country = request.form.get('country')
    genre = request.form.get('genre')
    description = request.form.get('description')
    authors = request.form.get('authors')
    actors = request.form.get('actors')
    tags = request.form.getlist('selectedTags')
    upload = request.files['uploaded_image']
    public = request.form.get('public') is not None

    if not title or not premiere or not country or not genre:
        flash('Title, premiere, country, genre cannot be empty.', category='error')
        return redirect(
            url_for(
                'movies.new',
                title=title,
                premiere=premiere,
                country=country,
                description=description,
                authors=authors,
                actors=actors,
                checked_tags=tags,
                public=public
            )
        )

    try:
        genre_id = Genre.query.filter_by(name=genre).first().id
    except AttributeError:
        flash('Choose genre from list.', category='error')
        return redirect(
            url_for(
                'movies.new',
                title=title,
                premiere=premiere,
                country=country,
                description=description,
                authors=authors,
                actors=actors,
                checked_tags=tags,
                public=public
            )
        )

    filename = upload.filename
    saved_filename = None
    if upload and '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png', 'gif']:
        filename = secure_filename(filename)
        upload.save(path.join('website/upload', filename))
        saved_filename = filename

    new_movie = Movie(
        title=title,
        premiere=premiere,
        country=country,
        genreid=genre_id,
        description=description,
        image_path=saved_filename,
        is_public=public,
        userid=current_user.id
    )

    if authors:
        for author_form in authors.split('\n'):
            parts = author_form.split()
            if len(parts) != 3:
                flash("Authors format must be '<role> <name> <surname>'.", category='error')
                return redirect(
                    url_for(
                        'movies.new',
                        title=title,
                        premiere=premiere,
                        country=country,
                        genre=genre,
                        description=description,
                        authors=authors,
                        actors=actors,
                        checked_tags=tags,
                        public=public
                    )
                )
            if Author.query.filter_by(role=parts[0], name=parts[1], surname=parts[2]).first() is None:
                author = Author(role=parts[0], name=parts[1], surname=parts[2])
                db.session.add(author)
                db.session.commit()

            author = Author.query.filter_by(role=parts[0], name=parts[1], surname=parts[2]).first()
            new_movie.authors.append(author)

    if actors:
        for actor_form in actors.split('\n'):
            parts = actor_form.split()
            if len(parts) != 2:
                flash("Actors format must be '<name> <surname>'.", category='error')
                return redirect(
                    url_for(
                        'movies.new',
                        title=title,
                        premiere=premiere,
                        country=country,
                        genre=genre,
                        description=description,
                        authors=authors,
                        actors=actors,
                        checked_tags=tags,
                        public=public
                    )
                )
            if Actor.query.filter_by(name=parts[0], surname=parts[1]).first() is None:
                actor = Actor(name=parts[0], surname=parts[1])
                db.session.add(actor)
                db.session.commit()

            actor = Actor.query.filter_by(name=parts[0], surname=parts[1]).first()
            new_movie.actors.append(actor)

    if len(tags) == 0:
        tags.append('watched')
    for tag_form in tags:
        tag = Tag.query.filter_by(name=tag_form).first()
        new_movie.tags.append(tag)

    db.session.add(new_movie)
    db.session.commit()

    if new_movie.is_public:
        return redirect(url_for('movies.public_movie', nickname=current_user.nickname, title=new_movie.title))
    else:
        return redirect(url_for('movies.private_movie', title=new_movie.title))


@movies.context_processor
def handle_context():
    from os import path
    return dict(path=path)
