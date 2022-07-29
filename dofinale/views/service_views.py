from flask import Blueprint, render_template, url_for, request, session, jsonify
from werkzeug.utils import redirect, secure_filename

from ..views.auth_views import login_required
from ..ptmodel import Image_transformer, Diagnosis

bp = Blueprint('service', __name__, url_prefix='/service')
model_path = './model'

@bp.route('/', methods=['GET','POST'])
@login_required
def service():
    if request.method == 'POST':
        f = request.files['file']
        # 저장할 경로 + 파일명
        print(f.filename)
        f.save(secure_filename(f.filename))
        result = Diagnosis(model_path,secure_filename(f.filename))
        return render_template('fileup.html', result=result)
    return render_template('fileup.html')