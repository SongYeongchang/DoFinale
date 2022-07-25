from datetime import datetime

from flask import Blueprint, url_for, request
from werkzeug.utils import redirect

from dofinale import db
from dofinale.models import *

bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/create/<int:userpost_id>', methods=('POST',))
def create(userpost_id):
    userpost = Userpost.query.get_or_404(userpost_id)
    content = request.form['content']
    usercomment = Usercomment(content=content, create_date=datetime.now())
    userpost.comment_set.append(usercomment)
    db.session.commit()
    return redirect(url_for('board.detail', userpost_id=userpost_id))