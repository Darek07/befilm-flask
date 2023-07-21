from .. import db


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100))
    role = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Author {self.name} {self.surname}>'
