from flask import Blueprint, request, jsonify, session
from kosenctfkit.models import db, Config, Team, User
from kosenctfkit.utils import error, login_required
from kosenctfkit.logging import logger
from kosenctfkit.uploader import uploader


user = Blueprint("user_", __name__)


@user.route("/register", methods=["POST"])
def register():
    if not Config.get().register_open:
        return error("Registration is closed")

    token = request.json.get("token", "").strip()
    if not token:
        return error("Token is required")

    username = request.json.get("username", "").strip()
    if not username:
        return error("Username is required")

    password = request.json.get("password", "").strip()
    if not password:
        return error("Password is required")

    team = Team.query.filter(Team.token == token).first()
    if not team:
        return error("The token is invalid")

    user = User.query.filter(User.name == username).first()
    if user:
        return error("The user `{}` already exists".format(username))

    # TODO: check number of members
    # TODO: send email for verification

    user = User()
    user.name = username
    user.password = password
    user.email = username + "@example.com"
    user.team_id = team.id
    user.verified = True

    team.valid = True

    db.session.add(team)
    db.session.add(user)
    db.session.commit()

    logger.log(
        ":heavy_plus_sign: `{}@{}` is registered".format(user.name, user.team.name)
    )
    return jsonify({"id": user.id, "name": user.name})


@user.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", "").strip()
    if not username:
        return error("Username is required")

    password = request.json.get("password", "").strip()
    if not password:
        return error("Password is required")

    user = User.query.filter(User.name == username).first()
    if not user:
        return error("User `{}` doesn't exist".format(username))

    if not user.check_password(password):
        return error("Invalid password")

    if not user.verified:
        return error("Unverified user")

    session["user_id"] = user.id
    return "", 204


@user.route("/password-update", methods=["POST"])
@login_required
def password_update(user):
    cur = request.json.get("current_password", "").strip()
    if not cur:
        return error("Current password required")

    new = request.json.get("new_password", "").strip()
    if not new:
        return error("New password required")

    if not user.check_password(cur):
        return error("Current password is invalid")

    user.password = new
    db.session.add(user)
    db.session.commit()

    return "", 204


@user.route("/upload-icon", methods=["POST"])
@login_required
def upload_icon(user):
    icon = request.json.get("icon", "").strip()
    if not icon:
        return error("Icon required")
    path = uploader.upload_icon(icon)
    if not path:
        return error("Failed to upload the icon")

    user.icon = path
    db.session.add(user)
    db.session.commit()
    return "", 204


@user.route("/logout")
def logout():
    _ = session.pop("user_id", None)
    return "", 204
