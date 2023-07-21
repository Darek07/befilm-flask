from sqlalchemy import func

from .. import db


class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    block_user = db.Column(db.Boolean, default=False, nullable=False)
    date_time = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    movie_title = db.Column(db.String(255))

    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('reports', lazy=True))

    def __repr__(self):
        return f'<Report {self.id}>'
