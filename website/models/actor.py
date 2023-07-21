from .. import db


class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100))

    def __repr__(self):
        return f'<Actor {self.name} {self.surname}>'
