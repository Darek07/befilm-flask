from sqlalchemy import func

from .. import db

movies_actors = db.Table('movie_actor',
                         db.Column('movieid', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
                         db.Column('actorid', db.Integer, db.ForeignKey('actors.id'), primary_key=True)
                         )

movies_authors = db.Table('movie_author',
                          db.Column('movieid', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
                          db.Column('authorid', db.Integer, db.ForeignKey('authors.id'), primary_key=True)
                          )

movies_tags = db.Table('movie_tag',
                       db.Column('movieid', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
                       db.Column('tagid', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
                       )


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    post_date = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    image_path = db.Column(db.String(255))
    title = db.Column(db.String(255), unique=True, nullable=False)
    premiere = db.Column(db.String(4), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=False, nullable=False)

    # Define the ManyToOne relationship to the Genre and User models
    genreid = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False)
    genre = db.relationship('Genre', backref=db.backref('movies', lazy=True))

    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('movies', lazy=True))

    # Define the ManyToMany relationships to the Actor, Author, and Tag models
    actors = db.relationship('Actor', secondary=movies_actors, backref=db.backref('movies', lazy=True))
    authors = db.relationship('Author', secondary=movies_authors, backref=db.backref('movies', lazy=True))
    tags = db.relationship('Tag', secondary=movies_tags, backref=db.backref('movies', lazy=True))

    def __repr__(self):
        return f'<Movie {self.title}>'
