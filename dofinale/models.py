from dofinale import db
from datetime import datetime

collation = 'utf8mb4_unicode_ci'

class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    userid = db.Column(db.String(20, collation), nullable=False)
    userpw = db.Column(db.String(20, collation), nullable=False)
    name = db.Column(db.String(20, collation), nullable=False)
    email = db.Column(db.String(30, collation), nullable=False)
    phone = db.Column(db.String(20, collation), nullable=False)
    address = db.Column(db.String(50, collation), nullable=False)
    scalp_type = db.Column(db.String(20, collation))
    signup_date = db.Column(db.DateTime, default = datetime.utcnow())

class Boards(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    board_name = db.Column(db.String(20, collation), nullable=False)

class Userpost(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    boards_id = db.Column(db.Integer, db.ForeignKey('boards.id', ondelete='CASCADE'))
    boards = db.relationship('Boards', backref=db.backref('post_set', cascade='all, delete-orphan'))
    subject = db.Column(db.String(200, collation), nullable=False)
    content = db.Column(db.Text(None, collation), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

class Usercomment(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    userpost_id = db.Column(db.Integer, db.ForeignKey('userpost.id', ondelete='CASCADE'))
    userpost = db.relationship('Userpost', backref=db.backref('comment_set', cascade='all, delete-orphan'))
    content = db.Column(db.Text(None, collation), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)