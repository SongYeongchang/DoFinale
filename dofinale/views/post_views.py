from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash, session
from werkzeug.utils import redirect

from dofinale import db
from dofinale.views.auth_views import login_required
from dofinale.forms import UserPostForm, UserCommentForm
from dofinale.models import Boards, Userpost

bp = Blueprint('post', __name__, url_prefix='/post')


# 커뮤니티 메인 페이지
@bp.route('/community/')
def community():
    return render_template('community.html')


# 게시물 리스트 페이지
@bp.route('/list/<int:board_id>/')
def _list(board_id):
    board = Boards.query.get_or_404(board_id)
    page = request.args.get('page', type=int, default=1)  # 페이지
    userpost_list = Userpost.query.filter_by(boards_id=board_id).order_by(Userpost.create_date.desc())
    userpost_list = userpost_list.paginate(page, per_page=10)
    return render_template('post/post_list.html', board=board, userpost_list=userpost_list)


# 게시물 생성 페이지
@bp.route('/create/<int:board_id>/', methods=('GET', 'POST'))
@login_required
def create(board_id):
    form = UserPostForm()
    board = Boards.query.get_or_404(board_id)
    if request.method == 'POST' and form.validate_on_submit():
        img_dir = None
        if request.files['file']:
            f = request.files['file']
            now = datetime.now()
            date_time = now.strftime("%Y%m%d%H%M%S")
            img_dir = f'{date_time}_user{str(session.get("user_id"))}.jpg'
            f.save('./dofinale/static/images/post/' + img_dir)
        userpost = Userpost(subject=form.subject.data, content=form.content.data, img_upload=img_dir, create_date=datetime.now(), boards=board, user=g.user)
        board.post_set.append(userpost)
        db.session.commit()
        return redirect(url_for('post.detail', userpost_id=userpost.id))
    return render_template('post/post_form.html', board=board, form=form)


# 게시물 내용 페이지
@bp.route('/detail/<int:userpost_id>/')
def detail(userpost_id):
    form = UserCommentForm()
    userpost = Userpost.query.get_or_404(userpost_id)
    return render_template('post/post_detail.html', userpost=userpost, form=form)

@bp.route('/delete/<int:userpost_id>/')
@login_required
def delete(userpost_id):
    userpost = Userpost.query.get_or_404(userpost_id)
    if g.user != userpost.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('post.detail', userpost_id=userpost_id))
    db.session.delete(userpost)
    db.session.commit()
    return redirect(url_for('post._list', board_id=userpost.boards_id))