from flask import Blueprint, render_template, url_for, request, session, jsonify, g
from werkzeug.utils import redirect, secure_filename

from dofinale.views.auth_views import login_required
from dofinale.ptmodel import Image_transformer, Diagnosis
from dofinale.models import Members
from dofinale import db


bp = Blueprint('service', __name__, url_prefix='/service')

model_path = './model'
userimage_path = './dofinale/static/images/user/'

gg=[]

# 두피 분석 페이지
@bp.route('/scalp_diagnosis', methods=['GET','POST'])
@login_required
def service():
    if request.method == 'POST':
        f = request.files['file']
        # 저장할 경로 + 파일명
        # print(f.filename)
        f.save(userimage_path + secure_filename(f.filename))
        # print('./dofinale/static/images/user/' + secure_filename(f.filename))
        result = Diagnosis(model_path, userimage_path + secure_filename(f.filename))
        g.user.scalp_type = result[-1]
        # result_text = ''
        # for i in result:
        #     result_text += i+'/'
        # result_text = result_text[:-1]
        # print('result_text:'+result_text)
        # g.user.scalp_type = result_text
        global gg
        gg.clear()
        for i in result:
            gg.append(i)
        print("gg>>",gg)
        print(g.user)
        db.session.commit()
        return render_template('scalp_diagnosis.html', resultbool=True)
    return render_template('scalp_diagnosis.html')

@bp.route('/survey/', methods=['GET','POST'])
def self_survey():
    return render_template('self_survey.html')

if __name__ == "__main__":
    pass
