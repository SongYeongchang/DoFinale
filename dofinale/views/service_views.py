from flask import Blueprint, render_template, url_for, request, session, jsonify, g
from werkzeug.utils import redirect, secure_filename
import json

from dofinale.views.auth_views import login_required
from dofinale.ptmodel import Image_transformer, Diagnosis
from dofinale.mlmodel import ml_survey
from dofinale import db


bp = Blueprint('service', __name__, url_prefix='/service')

model_path = './dofinale/static/aimodel/dl'
userimage_path = './dofinale/static/images/user/'



# 두피 분석 페이지
@bp.route('/diagnosis/', methods=['GET','POST'])
@login_required
def scalp_diagnosis():
    if request.method == 'POST':
        f = request.files['file']
        # 현재 세션 유저 고유 인덱스 번호로 이미지 파일명 저장
        img_dir = userimage_path + secure_filename(
            'user_' + str(session.get('user_id')) + '.jpg'
        )
        f.save(img_dir)
        result = Diagnosis(model_path, img_dir)
        g.user.scalp_type = result[-1] # 현재 세션 유저 DB에 두피 유형 예측 결과 저장
        db.session.commit()

        return redirect(url_for('service.diag_res'))
    return render_template('service/scalp_diagnosis.html')

# 두피 분석 결과 페이지
@bp.route('/diagnosis_res/', methods=['GET','POST'])
def diag_res():
    if request.method == 'POST':
        return redirect(url_for('service.scalp_diagnosis'))
    return render_template('service/diag_result.html')


# 자가 문진 챗봇 연결 페이지
@bp.route('/survey/', methods=['GET','POST'])
@login_required
def survey():
    if request.method == 'POST':

        surv_gen = request.form.get('gender')
        surv_age = request.form.get('age')
        surv_shampoo = request.form.get('frequency_shampoo', type=float)
        surv_perm = request.form.get('frequency_perm')
        surv_color = request.form.get('frequency_color')
        surv_condition = request.form.get('hair_condition')
        surv_product = request.form.get('product', type=int)

        surv_res = {
            "gender" : [surv_gen],
            "age" : [surv_age],
            "frequency_shampoo": [surv_shampoo],
            "frequency_perm": [surv_perm],
            "frequency_color": [surv_color],
            "hair_condition": [surv_condition],
            "product": [surv_product]
        }

        # print(surv_res)
        # print('-----------------')
        # for key, val in surv_res.items():
        #     print(f'{key} : {val} ({type(val[0])})')

        # 머신러닝 모델
        ml_res_str=''
        for symptom in ['alopecia','dandruff','pustule']:
            ml_res = ml_survey(symptom, surv_res)
            print(f'{symptom} 예측 : {ml_res}')
            if symptom=='alopecia' and ml_res[0][0]==1:
                ml_res_str += '탈모'
            elif symptom == 'dandruff' and ml_res[0][0] == 1:
                ml_res_str += '비듬'
            elif symptom == 'pustule' and ml_res[0][0] == 1:
                ml_res_str += '염증'

        if len(ml_res_str)==0:
            ml_res_str += '양호'
        elif len(ml_res_str)==4:
            ml_res_str = ml_res_str[:2]+','+ml_res_str[2:]
        elif len(ml_res_str)==6:
            ml_res_str = ml_res_str[:2]+','+ml_res_str[2:4]+','+ml_res_str[4:]


        g.user.ml_result = ml_res_str
        db.session.commit()

        return redirect(url_for('service.survey_res', surv_res=surv_res))
    return render_template('service/survey.html')

# 자가진단 결과 페이지
@bp.route('/survey_result/', methods=['GET','POST'])
def survey_res():
    return render_template('service/survey_result.html')


# 제품 소개 페이지
@bp.route('/product_list/', methods=['GET','POST'])
def product_list():
    with open('./dofinale/static/json_data/products.json', 'r', encoding="UTF-8") as file:
        products = json.load(file)
        return render_template('service/product_list.html', products=products)

# 서비스 소개 페이지
@bp.route('/about/')
def about():
    return render_template('about.html')