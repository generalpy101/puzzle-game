import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "db.sqlite"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    PORT = int(os.environ.get("PORT", 8000))
    JWT_EXPIRATION_MINUTES = 600
