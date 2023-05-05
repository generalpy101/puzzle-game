from functools import wraps

from flask import jsonify, request

from treasure_hunt.auth.utils import decode_jwt_token
from treasure_hunt.models import User


def jwt_login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            payload = decode_jwt_token(token)
            if not payload:
                return jsonify({"message": "Invalid token"}), 401

            user_id = payload.get("user_id")
            user = User.get_by_id(user_id)
            if not user:
                return jsonify({"message": "User not found"}), 401

        except:
            return jsonify({"message": "Token is invalid"}), 401

        return func(user, *args, **kwargs)

    return decorated
