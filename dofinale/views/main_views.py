from flask import Blueprint, render_template, url_for, request, session
from werkzeug.utils import redirect, secure_filename


bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def index():
    return redirect(url_for('post._list'))

# 추후 다시 구현 예정
# @bp.route('/fileUpload', methods=['GET','POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['file']
#         # 저장할 경로 + 파일명
#         print(f.filename)
#         f.save('data/'+secure_filename(f.filename))
#         return redirect(url_for('main.index'))
# 
#     return render_template('fileup.html')