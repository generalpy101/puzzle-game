import traceback
from functools import wraps

from app.auth.utils import decode_jwt_token
from app.db import User
from flask import jsonify, request
from jwt import ExpiredSignatureError


def jwt_login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            token = token.split(" ")[1]
            payload = decode_jwt_token(token)
            if not payload:
                return jsonify({"message": "Invalid token"}), 401

            user_id = payload.get("user_id")
            user = User.get_by_id(user_id)
            if not user:
                return jsonify({"message": "User not found"}), 401
        except ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except Exception as e:
            traceback.print_exc()
            return jsonify({"message": "Token is invalid"}), 401

        return func(user, *args, **kwargs)

    return decorated
