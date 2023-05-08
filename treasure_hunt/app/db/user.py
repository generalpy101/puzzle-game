from app.db import db
from app.db.roles import Role
from flask_login.mixins import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

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
    cleared_rooms = db.Column(db.String(255), default="")
    current_room = db.Column(db.Integer, default=0)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def cleared_rooms_list(self):
        if self.cleared_rooms:
            return self.cleared_rooms.split(",")
        return []

    @cleared_rooms_list.setter
    def cleared_rooms_list(self, room):
        rooms = self.cleared_rooms_list or []
        rooms.append(str(room))
        self.cleared_rooms = ",".join(rooms)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        for role in self.roles:
            if role.name == role_name:
                return True
        return False

    def to_dict(self):
        result = {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if "password" not in column.name
        }
        result["current_room"] = result["current_room"] if result["current_room"] else 0
        result["cleared_rooms"] = self.cleared_rooms_list
        return result

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    def __repr__(self):
        return f"<User {self.username}>"
