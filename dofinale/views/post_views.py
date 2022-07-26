from datetime import datetime

from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from .. import db
from ..forms import UserPostForm, UserCommentForm
from ..models import Userpost

bp = Blueprint('post', __name__, url_prefix='/post')

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    userpost_list = Userpost.query.order_by(Userpost.create_date.desc())
    userpost_list = userpost_list.paginate(page, per_page=10)
    return render_template('post/post_list.html', userpost_list=userpost_list)

@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = UserPostForm()
    if request.method == 'POST' and form.validate_on_submit():
        userpost = Userpost(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(userpost)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('post/post_form.html', form=form)

@bp.route('/detail/<int:userpost_id>/')
def detail(userpost_id):
    form = UserCommentForm()
    userpost = Userpost.query.get_or_404(userpost_id)
    return render_template('post/post_detail.html', userpost=userpost, form=form)