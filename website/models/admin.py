from .. import db


class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)

    # Define the OneToOne relationship to the User model for the admin user
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    admin_user = db.relationship('User', foreign_keys=[userid], backref=db.backref('admin', uselist=False))

    # Define the OneToOne relationship to the User model for the granting user
    granting_adminid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    granting_user = db.relationship('User', foreign_keys=[granting_adminid],
                                    backref=db.backref('admin_granted', uselist=False))

    def __repr__(self):
        return f'<Admin {self.user.nickname}>'
