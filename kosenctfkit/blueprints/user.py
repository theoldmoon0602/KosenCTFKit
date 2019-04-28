from flask import Blueprint, request, jsonify, session
from kosenctfkit.models import db, Config, Team, User
from kosenctfkit.utils import error, login_required
from kosenctfkit.logging import logger
from kosenctfkit.uploader import uploader


user = Blueprint("user", __name__)


@user.route("/register", methods=["POST"])
def register():
    token = request.json.get("token", "").strip()
    if not token:
        return error("token is required")

    username = request.json.get("username", "").strip()
    if not username:
        return error("username is required")

    password = request.json.get("password", "").strip()
    if not password:
        return error("password is required")

    team = Team.query.filter(Team.token == token).first()
    if not team:
        return error("the token is invalid")

    if not Config.get().register_open:
        return error("Registration is closed")

    user = User.query.filter(User.name == username).first()
    if user:
        return error("user `{}` already exists".format(username))

    # TODO: check number of members

    user = User()
    user.name = username
    user.password = password
    user.team_id = team.id

    team.valid = True

    db.session.add(team)
    db.session.add(user)
    db.session.commit()

    logger.log(
        ":heavy_plus_sign: `{}@{}` has just registered".format(
            user.name, user.team.name
        )
    )
    return jsonify({"id": user.id, "name": user.name})


@user.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", "").strip()
    if not username:
        return error("username is required")

    password = request.json.get("password", "").strip()
    if not password:
        return error("password is required")

    user = User.query.filter(User.name == username).first()
    if not user:
        return error("user `{}` doesn't exist".format(username))

    if not user.check_password(password):
        return error("invalid password")

    session["user_id"] = user.id
    return "", 204


@user.route("/password-update", methods=["POST"])
@login_required
def password_update(user):
    cur = request.json.get("current_password", "").strip()
    if not cur:
        return error("current_password required")

    new = request.json.get("new_password", "").strip()
    if not new:
        return error("new_password required")

    if not user.check_password(cur):
        return error("invalid current_password")

    user.password = new
    db.session.add(user)
    db.session.commit()

    return "", 204


@user.route("/upload-icon", methods=["POST"])
@login_required
def upload_icon(user):
    icon = request.json.get("icon", "").strip()
    if not icon:
        return error("icon required")
    path = uploader.upload_icon(icon)
    if not path:
        return error("failed to upload")

    user.icon = path
    db.session.add(user)
    db.session.commit()
    return "", 204


@user.route("/logout")
def logout():
    _ = session.pop("user_id", None)
    return "", 204
