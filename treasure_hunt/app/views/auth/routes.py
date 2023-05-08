from app.auth.decorators import jwt_login_required
from app.auth.utils import encode_jwt_token
from app.db import RoleFactory, User, db
from flask import Blueprint, abort, current_app, request
from flask_login import login_user
from werkzeug.exceptions import BadRequest, Unauthorized

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password1 = data.get("password1")
    password2 = data.get("password2")

    # @TODO to make this process easier using
    # modules such as marshmallow
    # validate values exist
    if not username or not email or not password1 or not password2:
        return BadRequest("Fields missing")

    if password1 != password2:
        return abort(400, "Passwords don't match")

    new_user = User(email=email, password=password1, username=username)
    new_user.roles.append(RoleFactory.create("user"))
    db.session.add(new_user)
    db.session.commit()
    return {"username": username, "email": email}, 201


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
    return {"token": token}


@auth_bp.route("/users", methods=["GET"])
@jwt_login_required
def protected(user: User):
    if user.has_role("admin") == False:
        return Unauthorized("Only accessible by admin")

    all_users = User.query.all()
    result = {}
    for current_user in all_users:
        result[current_user.id] = current_user.to_dict()

    return result
