from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dofinale import db

class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    userid = db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable=False)
    userpw = db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable=False)
    name = db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable=False)
    email = db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable=False)
    phone = db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable=False)
    address = db.Column(db.String(100, 'utf8mb4_unicode_ci'), nullable=False)
    scalp_type = db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable=False)
    start = db.Column(db.DateTime, default = datetime.utcnow())

    # 전화번호의 경우 '-'를 빼고 Integer로 저장하면 공간 절약도 되고 더 편하다고 생각할 수 있으나
    # 오히려 맨 앞에 0을 붙이기도 어렵고 숫자 크기만 엄청 커진다.
    # 그래서 그냥 String으로 저장하는 게 편하다.
    # 'utf8mb4_unicode_ci'의 매개변수명은 collation

class Boards(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(200, 'utf8mb4_unicode_ci'), nullable=False)
    content = db.Column(db.Text(None, 'utf8mb4_unicode_ci'), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)