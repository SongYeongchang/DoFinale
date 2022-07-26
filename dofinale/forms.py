from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class UserCreateForm(FlaskForm):
    userid = StringField('아이디',validators=[DataRequired(),Length(min=3,max=20)])
    userpw1 = PasswordField('비밀번호',validators=[DataRequired()])
    userpw2 = PasswordField('비밀번호 확인', validators=[DataRequired(), EqualTo('userpw1', '비밀번호가 일치하지 않습니다.')])
    name = StringField('이름',validators=[DataRequired(),Length(min=3,max=20)])
    email = EmailField('이메일',validators=[DataRequired(),Email()])
    phone = StringField('전화번호',validators=[DataRequired(),Length(min=11,max=20)])
    address = StringField('주소',validators=[DataRequired(),Length(min=3,max=100)])

class UserPostForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class UserCommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])