import json

from app.auth.decorators import jwt_login_required
from app.db import User, db
from app.utils import ROOM_PASSWORDS
from flask import Blueprint, current_app, jsonify, request
from werkzeug.exceptions import BadRequest, HTTPException

core_bp = Blueprint("core", __name__)


@core_bp.errorhandler(400)
def handle_http_exceptions(err):
    """
    Custom handler for HTTP exceptions.
    Returns JSON output instead of HTML.
    """
    response = err.get_response()
    payload = {
        "status_code": err.code,
        "error": err.name,
        "message": err.description,
    }
    response.data = json.dumps(payload)
    response.content_type = "application/json"
    return response


@core_bp.route("/user_info", methods=["GET"])
@jwt_login_required
def user_info(user: User):
    return jsonify(user.to_dict())


@core_bp.route("/validate_room", methods=["POST"])
@jwt_login_required
def validate_room_password(user: User):
    data = request.get_json()
    room = data.get("room")
    password = data.get("password")

    try:
        room = int(room)
    except ValueError:
        return BadRequest("Room must be an integer")

    if not room or not password:
        return BadRequest("Missing room or password")

    if room not in ROOM_PASSWORDS:
        return BadRequest("Invalid room")

    if ROOM_PASSWORDS[room] != password:
        return jsonify({"valid": False})

    user.cleared_rooms_list = room
    user.current_room = room
    db.session.add(user)
    db.session.commit()
    return jsonify({"valid": True})


@core_bp.route("/game_over", methods=["GET"])
@jwt_login_required
def game_over(user: User):
    user.current_room = 0
    user.cleared_rooms = ""
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Game over"})
