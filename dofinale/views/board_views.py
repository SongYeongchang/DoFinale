from flask import Blueprint, render_template

from dofinale.models import *

bp = Blueprint('board', __name__, url_prefix='/board')


@bp.route('/list/')
def _list():
    userpost_list = Userpost.query.order_by(Userpost.create_date.desc())
    return render_template('temp.html', userpost_list=userpost_list)

@bp.route('/detail/<int:userpost_id>/')
def detail(userpost_id):
    userpost = Userpost.query.get_or_404(userpost_id)
    return render_template('temp_detail.html', userpost=userpost)