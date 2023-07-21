from sqlalchemy import func
from flask_login import UserMixin

from .. import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    join_date = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    email = db.Column(db.String(120), unique=True, nullable=False)
    nickname = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.nickname}>'
