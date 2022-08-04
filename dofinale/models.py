from dofinale import db
from datetime import datetime

# 이모지를 포함한 유니코드 인코딩
collation = 'utf8mb4_unicode_ci'

# 회원 테이블
class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    userid = db.Column(db.String(20, collation), unique=True, nullable=False)
    userpw = db.Column(db.BINARY(60), nullable=False)
    name = db.Column(db.String(20, collation), nullable=False)
    email = db.Column(db.String(30, collation), unique=True, nullable=False)
    phone = db.Column(db.String(20, collation), unique=True, nullable=False)
    address = db.Column(db.String(50, collation), nullable=False)
    scalp_type = db.Column(db.String(20, collation))
    signup_date = db.Column(db.DateTime, default = datetime.utcnow())

# 게시판 모델은 당장 오류가 있어 나중에 다시 추가할 예정
# class Boards(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
#     board_name = db.Column(db.String(20, collation), nullable=False)

# 회원 게시물 테이블
class Userpost(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    subject = db.Column(db.String(200, collation), nullable=False)
    content = db.Column(db.Text(None, collation), nullable=False)
    # 게시판 모델과 연동은 나중에 다시 구현할 예정
    # boards_id = db.Column(db.Integer, db.ForeignKey('boards.id', ondelete='CASCADE'), nullable=True, server_default='1')
    # boards = db.relationship('Boards', backref=db.backref('post_set', cascade='all, delete-orphan'))
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('members.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('Members', backref=db.backref('post_set'))

# 회원 댓글 테이블
class Usercomment(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    userpost_id = db.Column(db.Integer, db.ForeignKey('userpost.id', ondelete='CASCADE'))
    userpost = db.relationship('Userpost', backref=db.backref('comment_set', cascade='all, delete-orphan'))
    content = db.Column(db.Text(None, collation), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('members.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('Members', backref=db.backref('comment_set'))