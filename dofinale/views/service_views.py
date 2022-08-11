from flask import Blueprint, render_template, url_for, request, session, jsonify, g
from werkzeug.utils import redirect, secure_filename
import json

from dofinale.views.auth_views import login_required
from dofinale.ptmodel import Image_transformer, Diagnosis
from dofinale import db


bp = Blueprint('service', __name__, url_prefix='/service')

model_path = './model'
userimage_path = './dofinale/static/images/user/'

gg=[]

# 두피 분석 페이지
@bp.route('/diagnosis/', methods=['GET','POST'])
@login_required
def scalp_diagnosis():
    if request.method == 'POST':
        f = request.files['file']
        img_dir = userimage_path + secure_filename(f.filename) # 두피 이미지 저장 경로
        f.save(img_dir)
        result = Diagnosis(model_path, img_dir)
        g.user.scalp_type = result[-1] # 현재 세션 유저 DB에 두피 유형 예측 결과 저장
        db.session.commit()

        global gg
        gg.clear()
        for i in result:
            gg.append(i)
        print("gg>>", gg)

        return render_template('service/scalp_diagnosis.html', btnclick=True)
    return render_template('service/scalp_diagnosis.html')


# 자가 문진 챗봇 연결 페이지
@bp.route('/survey/', methods=['GET','POST'])
@login_required
def survey():
    if request.method == 'POST':
        return render_template('service/survey.html', btnclick=True)
    return render_template('service/survey.html')


# 제품 소개 페이지
@bp.route('/product_list/', methods=['GET','POST'])
def product_list():
    with open('./dofinale/static/json_data/products.json', 'r', encoding="UTF-8") as file:
        products = json.load(file)
        return render_template('service/product_list.html', products=products)