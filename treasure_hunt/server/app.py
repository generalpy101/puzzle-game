from flask import Flask
from views.auth import auth_bp

from treasure_hunt.auth import login_manager
from treasure_hunt.models import db, init_db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///treasure_hunt.db"
app.secret_key = "abc"
db.init_app(app)
login_manager.__init__(app)
init_db(app)

app.register_blueprint(auth_bp, url_prefix="/auth")


@app.route("/")
def index():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(port=8000, debug=True)
