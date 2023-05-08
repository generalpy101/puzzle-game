from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    with app.app_context():
        db.create_all()


from .roles import Role, RoleFactory
from .user import User
