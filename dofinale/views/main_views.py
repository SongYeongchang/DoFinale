from flask import Blueprint, render_template, url_for, request, session, g
from werkzeug.utils import redirect, secure_filename

from ..models import Members

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
    return redirect(url_for('post._list'))

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

@bp.route('/fileUpload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # 저장할 경로 + 파일명
        print(f.filename)
        f.save('data/'+secure_filename(f.filename))
        return redirect(url_for('main.index'))

    return render_template('fileup.html')