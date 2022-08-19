from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, Email

# 로그인 폼
class UserLoginForm(FlaskForm):
    userid = StringField('아이디', validators=[DataRequired('아이디는 필수 입력 항목입니다.'), Length(min=3, max=25)])
    userpw = PasswordField('비밀번호', validators=[DataRequired('비밀번호는 필수 입력 항목입니다.')])

# 회원가입 폼
class UserCreateForm(FlaskForm):
    userid = StringField('아이디',validators=[DataRequired('아이디는 필수 입력 항목입니다.'), Length(min=3,max=25)])
    userpw1 = PasswordField('비밀번호',validators=[DataRequired('비밀번호는 필수 입력 항목입니다.')])
    userpw2 = PasswordField('비밀번호 확인', validators=[DataRequired('비밀번호는 필수 입력 항목입니다.'), EqualTo('userpw1', '비밀번호가 일치하지 않습니다.')])
    name = StringField('이름',validators=[DataRequired('이름은 필수 입력 항목입니다.'), Length(min=3,max=20)])
    email = EmailField('이메일',validators=[DataRequired('이메일은 필수 입력 항목입니다.'), Email()])
    phone = StringField('전화번호',validators=[DataRequired('연락처는 필수 입력 항목입니다.'), Length(min=11,max=20)])
    address = StringField('주소',validators=[DataRequired('주소는 필수 입력 항목입니다.'), Length(min=3,max=100)])

# 게시물 등록 폼
class UserPostForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수 입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])

# 댓글 등록 폼
class UserCommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])