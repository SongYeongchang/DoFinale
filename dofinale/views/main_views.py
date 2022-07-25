from flask import Blueprint, render_template, url_for, request, session, g
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect, secure_filename

from dofinale.forms import UserCreateForm
from dofinale.models import Members
from dofinale import db

bp = Blueprint('main', __name__, url_prefix='/')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = user_id

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login',methods=('GET','POST'))
def login():
    if request.method == 'POST':
        user = Members.query.filter_by(userid=request.form.get('id')).first()

        if not user:
            print('존재하지 않는 유저')
        elif user.userpw == request.form.get('pw'):
            session.clear()
            session['user_id'] = user.userid
            print('로그인 성공')
            return redirect(url_for('main.index'))
        else:
            return render_template('login.html')

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@bp.route('/signup',methods=('GET','POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = Members.query.filter_by(userid=form.userid.data).first()
        if not user:
            user = Members(userid = form.userid.data,
                           userpw = form.userpw1.data,
                           name = form.name.data,
                           email = form.email.data,
                           phone = form.phone.data,
                           address = form.address.data
                           )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.login'))
        else:
            print('이미 존재하는 유저입니다.')

    return render_template('signup.html',form=form)

@bp.route('/fileUpload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # 저장할 경로 + 파일명
        print(f.filename)
        f.save('data/'+secure_filename(f.filename))
        return redirect(url_for('main.index'))

    return render_template('fileup.html')