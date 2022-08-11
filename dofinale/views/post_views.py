from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from dofinale import db
from dofinale.views.auth_views import login_required
from dofinale.forms import UserPostForm, UserCommentForm
from dofinale.models import Userpost

bp = Blueprint('post', __name__, url_prefix='/post')


# 커뮤니티 메인 페이지
@bp.route('/community/')
def community():
    return render_template('community.html')


# 게시물 리스트 페이지
@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    userpost_list = Userpost.query.order_by(Userpost.create_date.desc())
    userpost_list = userpost_list.paginate(page, per_page=10)
    return render_template('post/post_list.html', userpost_list=userpost_list)


# 게시물 생성 페이지
@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = UserPostForm()
    if request.method == 'POST' and form.validate_on_submit():
        userpost = Userpost(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(userpost)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('post/post_form.html', form=form)


# 게시물 내용 페이지
@bp.route('/detail/<int:userpost_id>/')
def detail(userpost_id):
    form = UserCommentForm()
    userpost = Userpost.query.get_or_404(userpost_id)
    return render_template('post/post_detail.html', userpost=userpost, form=form)