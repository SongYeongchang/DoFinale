from datetime import datetime
from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect

from .. import db
from ..forms import UserCommentForm
from ..models import Userpost, Usercomment

bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/create/<int:userpost_id>', methods=('POST',))
def create(userpost_id):
    form = UserCommentForm()
    userpost = Userpost.query.get_or_404(userpost_id)
    if form.validate_on_submit():
        content = request.form['content']
        usercomment = Usercomment(content=content, create_date=datetime.now())
        userpost.comment_set.append(usercomment)
        db.session.commit()
        return redirect(url_for('post.detail', userpost_id=userpost_id))
    return render_template('post/post_detail.html', userpost=userpost, form=form)