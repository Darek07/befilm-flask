from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import re

from . import db
from .models.user import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        password = request.form.get('password')

        user = User.query.filter_by(nickname=nickname).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash('Logged in!', category='success')
                return redirect(url_for('categories.watched'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('User with the given nickname does not exist.', category='error')

        return render_template('login.html', login=True, nickname=nickname)

    return render_template('login.html', login=True)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        email = request.form.get('email')
        password = request.form.get('password')

        email_exists = User.query.filter_by(email=email).first()
        user_exists = User.query.filter_by(nickname=nickname).first()

        if email_exists:
            flash('Email is already taken.', category='error')
        elif user_exists:
            flash('Nickname is already taken.', category='error')
        elif len(nickname) < 3:
            flash('Nickname is too short.', category='error')
        elif not re.match(r'^[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+\.[a-zA-Z]*$', email):
            flash('Email is invalid.', category='error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters long.', category='error')
        else:
            new_user = User(nickname=nickname, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Signed up successfully!', category='success')
            return redirect(url_for('categories.watched'))

        return render_template('register.html', login=False, nickname=nickname, email=email)

    return render_template('register.html', login=False)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))
