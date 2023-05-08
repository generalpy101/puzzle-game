from app.db import db


class RoleEnum:
    USER = "user"
    ADMIN = "admin"


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return f"<Role {self.name}>"


class RoleFactory:
    @staticmethod
    def create(name):
        if name == RoleEnum.USER:
            return Role.query.filter_by(name=RoleEnum.USER).first()
        elif name == RoleEnum.ADMIN:
            return Role.query.filter_by(name=RoleEnum.ADMIN).first()
        else:
            return None
