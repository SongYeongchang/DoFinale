from flask import Blueprint, url_for, render_template, flash, request, session, g
from flask_bcrypt import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
import functools

from dofinale import db
from dofinale.forms import UserCreateForm, UserLoginForm
from dofinale.models import Members

bp = Blueprint('auth', __name__, url_prefix='/auth')

# 로그인이 필요한 기능에 적용
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = Members.query.get(user_id)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = Members.query.filter_by(userid=form.userid.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.userpw, form.userpw.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            else:
                print('로그인 완료')
                return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.route('/logout/')
def logout():
    session.clear()
    print('로그아웃 완료')
    return redirect(url_for('main.index'))

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = Members.query.filter_by(userid=form.userid.data).first()
        if not user:
            user = Members(userid = form.userid.data,
                           userpw = generate_password_hash(form.userpw1.data),
                           name = form.name.data,
                           email = form.email.data,
                           phone = form.phone.data,
                           address = form.address.data
                           )
            db.session.add(user)
            db.session.commit()
            print('가입 완료')
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 유저입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/delete_user/', methods=('GET', 'POST'))
def delete_user():
    if request.method == 'POST':
        db.session.delete(g.user)
        db.session.commit()
        session.clear()
        print('탈퇴 처리 완료')
        return redirect(url_for('main.index'))
    return render_template('auth/delete_user.html')