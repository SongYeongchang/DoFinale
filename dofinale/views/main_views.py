from flask import Blueprint, render_template, url_for, request, session, jsonify
from werkzeug.utils import redirect, secure_filename


bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def index():
    return redirect(url_for('main.intro'))

@bp.route('/intro/')
def intro():
    return render_template('intro.html')


@bp.route('/cover/')
def cover():
    return render_template('cover.html')
