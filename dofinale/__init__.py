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

    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app