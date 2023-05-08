from app.auth import login_manager
from app.config import Config
from app.db import db
from app.views.auth.routes import auth_bp
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
