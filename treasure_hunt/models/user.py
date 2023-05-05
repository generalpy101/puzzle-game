from flask_login.mixins import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from treasure_hunt.models import db
from treasure_hunt.models.roles import Role

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True)
    roles = db.relationship(
        "Role", secondary="roles_users", backref=db.backref("users", lazy="dynamic")
    )

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        for role in self.roles:
            if role.name == role_name:
                return True
        return False

    @staticmethod
    def get_by_id(self, id):
        return User.query.get(id)

    def __repr__(self):
        return f"<User {self.username}>"
