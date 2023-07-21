from .. import db


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)

    # Define the ManyToOne relationship to the User and Movie models
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('likes', lazy=True))

    movieid = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    movie = db.relationship('Movie', backref=db.backref('likes', lazy=True))

    def __repr__(self):
        return f'<Like {self.id}>'
