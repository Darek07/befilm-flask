from functools import wraps
from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_required, current_user

from . import db
from .models.report import Report
from .models.user import User
from .models.admin import Admin
from .models.movie import Movie

admin = Blueprint('admin', __name__)


def admin_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not current_user.admin:
            return redirect(url_for('categories.watched'))

        return view_func(*args, **kwargs)

    return decorated_view


@admin.route('/panel')
@login_required
@admin_required
def panel():
    return render_template('admin_panel.html', chosen='Admin Panel')


@admin.route('/reports')
@login_required
@admin_required
def reports():
    report_history = Report.query.order_by(Report.date_time.desc()).all()
    return render_template('reports.html', chosen='Report History', reports=report_history)


@admin.route('/blocked')
@login_required
@admin_required
def blocked():
    blocked_history = Report.query.filter_by(block_user=True).all()
    return render_template('reports.html', chosen='Blocked Users', reports=blocked_history)


@admin.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    print('add')
    if request.method == 'POST':
        print('add...')
        nickname = request.form.get('nickname')
        user = User.query.filter_by(nickname=nickname).first()
        new_admin = Admin(userid=user.id, granting_adminid=current_user.id)
        db.session.add(new_admin)
        db.session.commit()

    users = User.query.filter(User.nickname != current_user.nickname, User.id.not_in(
        Admin.query.with_entities(Admin.userid).subquery()
    )).all()
    return render_template('admin_add.html', chosen='Add admin', users=users)


@admin.route('/create_report', methods=['GET', 'POST'])
@login_required
@admin_required
def create_report():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        title = request.form.get('title')
        description = request.form.get('description')
        submit_value = request.form.get('submit')

        userid = User.query.filter_by(nickname=nickname).first().id
        if description:
            report = Report(description=description, movie_title=title, userid=userid,
                            block_user=(submit_value == 'Block user'))
            movie = Movie.query.filter_by(title=title, userid=userid).first()
            movie.is_public = False
            db.session.add(report)
            db.session.commit()
            return redirect(url_for('admin.reports'))
        else:
            flash('Description field cannot be empty.', category='error')

    if 'nickname' not in request.args:
        public_movies = (
            Movie.query
            .filter_by(is_public=True)
            .join(User)
            .filter(User.nickname != current_user.nickname)
            .with_entities(Movie)
            .order_by(Movie.post_date.desc())
            .all()
        )
        return render_template('records.html', chosen='Create Report', movies=public_movies)

    nickname = request.args.get('nickname')
    reports_amount = len(User.query.filter_by(nickname=nickname).first().reports)
    return render_template('create_report.html', chosen='Create Report', **request.args, reports=reports_amount)


@admin.post('/blocked')
@login_required
@admin_required
def update_block_status():
    block = request.form.get('block')
    nickname = request.form.get('nickname')
    title = request.form.get('title')
    if block == 'Block':
        return redirect(url_for('admin.create_report', nickname=nickname, title=title))

    user = User.query.filter_by(nickname=nickname).first()
    for report in user.reports:
        report.block_user = False

    db.session.commit()
    return redirect(url_for('admin.blocked'))
