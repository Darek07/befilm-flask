from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'BeFilm'
DB_USERNAME = 'postgres'
DB_PASSWORD = ''


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '6f6a9f3b3c1247c11446a87dcd81defad72d53faa7f35fc7bcc8ea3ff5524811'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{DB_NAME}'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .categories import categories
    from .movies import movies
    from .admin import admin

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(categories, url_prefix='/categories/')
    app.register_blueprint(movies, url_prefix='/movies/')
    app.register_blueprint(admin, url_prefix='/admin/')

    from .models.actor import Actor
    from .models.admin import Admin
    from .models.author import Author
    from .models.genre import Genre
    from .models.like import Like
    from .models.movie import Movie
    from .models.report import Report
    from .models.tag import Tag
    from .models.user import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


def create_database(app):
    with app.app_context():
        db.create_all()

        from .models.admin import Admin
        from .models.user import User
        from werkzeug.security import generate_password_hash
        if len(Admin.query.all()) == 0:
            print('CHANGE FIRST ADMIN DATA FOR APPLICATION SAFETY!')
            user = User(nickname='admin', email='admin@admin.com', password=generate_password_hash('admin', method='sha256'))
            db.session.add(user)
            db.session.commit()
            admin = Admin(userid=User.query.filter_by(nickname=user.nickname).first().id)
            db.session.add(admin)
            db.session.commit()
