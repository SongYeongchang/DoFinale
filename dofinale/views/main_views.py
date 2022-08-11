from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def index():
    return redirect(url_for('main.intro'))

@bp.route('/intro/')
def intro():
    return render_template('intro.html', isbgvid=True)