"""Module implements auth functionality."""

from flask import request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restx import Resource, fields, Namespace

from werkzeug.security import generate_password_hash, check_password_hash

from app import app, api, db
from app.models import User, Role
from app.schemas.users import UserWithRoleSchema
from app.resources.models.auth import login_response, register_response, logout_response
from app.resources.models.users import user_info


auth_api = Namespace("auth", "Auth routes")


login_manager = LoginManager()
login_manager.init_app(app)


auth_model = api.model("Auth Model", {
    "username": fields.String(example="username"),
    "password": fields.String(example="password")
})


@login_manager.user_loader
def load_user(user_id):
    """Returns User object by user_id."""
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    """Returns message if no authorized."""
    return {"message": "Unauthenticated."}, 401


@auth_api.route("/user")
class UserRoute(Resource):

    @login_required
    @auth_api.response(200, "Success", user_info)
    @auth_api.response(401, "Unauthenticated")
    def get(self):
        return UserWithRoleSchema.from_orm(current_user).dict()


@auth_api.route("/register")
class RegisterRoute(Resource):

    @auth_api.expect(auth_model)
    @auth_api.response(200, "Success", register_response)
    @auth_api.response(400, "Bad request")
    @auth_api.response(401, "Unauthenticated")
    def post(self):
        username = request.json.get("username")
        password = request.json.get("password")

        if not username or not password:
            return {"message": "Username and password is required fields."}, 400

        if User.query.filter_by(username=username).first():
            return {"message": "Username is already used."}, 400

        password_hash = generate_password_hash(password)

        user_role = Role.query.filter_by(name="user").first()

        user = User(username=username, password=password_hash, role_id=user_role.id)

        db.session.add(user)
        db.session.commit()

        return {"message": "Registered successfully."}, 200


@auth_api.route("/login")
class LoginRoute(Resource):

    @auth_api.expect(auth_model)
    @auth_api.response(200, "Success", login_response)
    @auth_api.response(400, "Bad request")
    @auth_api.response(401, "Unauthenticated")
    def post(self):
        username = request.json.get("username")
        password = request.json.get("password")

        if not username or not password:
            return {"message": "Username and password is required fields."}, 400

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            app.logger.info("%s logged in successfully.", user.username)

            return {"message": "Authentication done successfully."}, 200

        app.logger.info("%s failed logging.", username)
        return {"message": "Incorrect username or password."}, 400


@auth_api.route("/logout")
class LogoutRoute(Resource):

    @login_required
    @auth_api.response(200, "Success", logout_response)
    @auth_api.response(401, "Unauthenticated")
    def post(self):
        logout_user()
        return {"message": "Logout done successfully."}, 200


api.add_namespace(auth_api)
