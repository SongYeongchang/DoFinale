from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT, SECRET_KEY

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    app.debug = True

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models
    
    # 블루프린트
    from .views import main_views, post_views, comment_views, auth_views, chatbot_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(post_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(auth_views.bp)
    # app.register_blueprint(chatbot_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app