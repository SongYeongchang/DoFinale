from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from dofinale import db
from dofinale.forms import UserCreateForm
from dofinale.models import Members

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=('GET', 'POST'))
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
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 유저입니다.')
    return render_template('auth/signup.html', form=form)