from datetime import datetime, timedelta

import jwt
from flask import current_app


def encode_jwt_token(user_id, username):
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.utcnow()
        + timedelta(minutes=current_app.config["JWT_EXPIRATION_MINUTES"]),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_jwt_token(token):
    payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    if "exp" not in payload:
        raise jwt.InvalidTokenError("Token does not contain expiration time")
    if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
        raise jwt.ExpiredSignatureError("Token has expired")
    return payload
