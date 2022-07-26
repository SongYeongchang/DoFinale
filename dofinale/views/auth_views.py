from flask import Blueprint, url_for, render_template, flash, request, session
from flask_bcrypt import generate_password_hash, check_password_hash
# from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from dofinale import db
from dofinale.forms import UserCreateForm, UserLoginForm
from dofinale.models import Members

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = Members.query.filter_by(userid=form.userid.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.userpw.encode('utf-8'), form.userpw.data.encode('utf-8')):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            print(form.userpw.data)
            print(user.userpw)
            session.clear()
            session['user_id'] = user.userid
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = Members.query.filter_by(userid=form.userid.data).first()
        if not user:
            user = Members(userid = form.userid.data,
                           userpw = generate_password_hash(form.userpw1.data).decode('utf-8'),
                           name = form.name.data,
                           email = form.email.data,
                           phone = form.phone.data,
                           address = form.address.data
                           )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 유저입니다.')
    return render_template('auth/signup.html', form=form)