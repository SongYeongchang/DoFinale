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

@bp.route('/', methods=['GET','POST'])
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
        global gg
        # for i in result:
        #     gg.append(i)
        gg.append(result[-1])
        print("gg>>",gg)
        print(g.user)
        db.session.commit()
        return render_template('fileup.html', resultbool=True)
    return render_template('fileup.html')

if __name__ == "__main__":
    pass
