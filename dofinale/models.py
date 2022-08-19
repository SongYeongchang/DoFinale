from dofinale import db
from datetime import datetime

# 이모지 사용이 가능한 인코딩으로 변경
collation = 'utf8mb4_unicode_ci'


# 회원 테이블 모델
class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    userid = db.Column(db.String(20, collation), unique=True, nullable=False) # 아이디
    userpw = db.Column(db.BINARY(60), nullable=False) # 비밀번호
    name = db.Column(db.String(20, collation), nullable=False) # 이름
    email = db.Column(db.String(30, collation), unique=True, nullable=False) # 이메일 주소
    phone = db.Column(db.String(20, collation), unique=True, nullable=False) # 연락처
    address = db.Column(db.String(50, collation), nullable=False) # 거주지 주소
    scalp_type = db.Column(db.String(20, collation), default="진단 이력 없음") # 두피 유형
    signup_date = db.Column(db.DateTime, default = datetime.utcnow()) # 가입 날짜
    ml_result = db.Column(db.String(20, collation), default="진단 이력 없음")  # 설문 결과


# 두피 유형별 게시판 테이블 모델
class Boards(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    board_name = db.Column(db.String(20, collation), nullable=False) # 게시판명


# 회원 게시물 테이블 모델
class Userpost(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    subject = db.Column(db.String(200, collation), nullable=False) # 게시물 제목
    content = db.Column(db.Text(None, collation), nullable=False) # 게시물 내용
    img_upload = db.Column(db.String(200, collation), nullable=True) # 첨부 이미지 주소
    create_date = db.Column(db.DateTime(), nullable=False) # 게시물 생성 날짜


    # ForeignKey를 통해 Boards의 id를 저장
    boards_id = db.Column(db.Integer, db.ForeignKey('boards.id', ondelete='CASCADE'), nullable=False)
    # Boards 모델과 관계 설정
    # backref(역참조)를 통해 '(Boards 객체).post_set'은 해당 게시판의 게시물 세트를 보여줌
    # delete-orphan : 게시판이 삭제될 경우 해당 게시판에 속한 모든 게시물도 같이 삭제
    boards = db.relationship('Boards', backref=db.backref('post_set', cascade='all, delete-orphan', order_by='Userpost.create_date.desc()'))


    # ForeignKey를 통해 Members의 id를 저장
    user_id = db.Column(db.Integer, db.ForeignKey('members.id', ondelete='CASCADE'), nullable=False)
    # Members 모델과 관계 설정
    # backref(역참조)를 통해 '(Members 객체).post_set'은 해당 유저의 모든 게시물 세트를 보여줌
    # delete-orphan : 유저가 탈퇴할 경우 해당 유저의 모든 게시물도 같이 삭제
    user = db.relationship('Members', backref=db.backref('post_set', cascade='all, delete-orphan'))


# 회원 댓글 테이블 모델
class Usercomment(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    content = db.Column(db.Text(None, collation), nullable=False) # 댓글 내용
    create_date = db.Column(db.DateTime(), nullable=False) # 댓글 생성 날짜

    # ForeignKey를 통해 Userpost의 id를 저장
    userpost_id = db.Column(db.Integer, db.ForeignKey('userpost.id', ondelete='CASCADE'))
    # Userpost 모델과 관계 설정
    # backref(역참조)를 통해 '(Userpost 객체).comment_set'은 해당 게시물의 댓글 세트를 보여줌
    # delete-orphan : 게시물이 삭제될 경우 연동된 댓글도 같이 삭제
    userpost = db.relationship('Userpost', backref=db.backref('comment_set', cascade='all, delete-orphan'))

    # ForeignKey를 통해 Members의 id를 저장
    user_id = db.Column(db.Integer, db.ForeignKey('members.id', ondelete='CASCADE'), nullable=False)
    # Members 모델과 관계 설정
    # backref(역참조)를 통해 '(Members 객체).comment_set'은 해당 유저의 댓글 세트를 보여줌
    # delete-orphan : 유저가 탈퇴할 경우 해당 유저의 모든 댓글도 같이 삭제
    user = db.relationship('Members', backref=db.backref('comment_set', cascade='all, delete-orphan'))