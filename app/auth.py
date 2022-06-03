"""Module implemets auth functionality."""

from flask import request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required

from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from app.database.models import User, Role


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Returns User object by user_id."""
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    """Returns message if no authorized."""
    return {"message": "Unauthenticated."}, 401


@app.route("/register", methods=["POST"])
def register():
    """Registering user."""
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password is required fields."}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username is already used."}), 400

    password_hash = generate_password_hash(password)

    user_role = Role.query.filter_by(name="user").first()

    user = User(username=username, password=password_hash, role_id=user_role.id)

    db.session.add(user)
    db.session.commit()

    return jsonify({"username": username})


@app.route("/login", methods=["POST"])
def login():
    """Logging user in."""
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password is required fields."}), 400

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)

        return jsonify({"message": "Authentication successfully."}), 200

    return jsonify({"message": "Incorrect username or password."}), 400


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    """Logging user out."""
    logout_user()
    return jsonify({"message": "Logout done successfully."}), 200

