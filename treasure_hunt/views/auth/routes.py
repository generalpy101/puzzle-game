import jwt
from flask import Blueprint, current_app, request
from flask_login import login_user

from treasure_hunt.auth.decorators import jwt_login_required
from treasure_hunt.auth.utils import encode_jwt_token
from treasure_hunt.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username).first()
    if user is None or not user.verify_password(password):
        return {"message": "Invalid username or password"}, 401
    login_user(user)
    token = encode_jwt_token(user.id, user.username)
    return {"token": token.decode("utf-8")}


@auth_bp.route("/protected")
@jwt_login_required
def protected(user):
    return {"message": f"Hello {user.username}"}
