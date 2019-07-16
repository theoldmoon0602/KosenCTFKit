from flask import Blueprint, request, jsonify, session, current_app
import os.path
from sqlalchemy.exc import IntegrityError
from kosenctfkit.models import db, Config, Team, User
from kosenctfkit.utils import error, login_required
from kosenctfkit.logging import logger
from kosenctfkit.uploader import uploader


user = Blueprint("user_", __name__)


def send_passwordreset_mail(user: User):
    import smtplib
    from email.mime.text import MIMEText

    from_address = current_app.config["EMAIL"]
    to_address = user.email

    msg = MIMEText(
        """Hi, {username}.
Your password reset link is here: {address}
    """.format(
            username=user.name,
            address=os.path.join(request.url_root, "#/reset/" + user.reset_token),
        )
    )
    msg["Subject"] = "{} password reset issue".format(current_app.config["CTF_NAME"])
    msg["From"] = from_address
    msg["To"] = to_address

    s = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    s.ehlo()
    s.login(from_address, current_app.config["EMAIL_PASSWORD"])
    s.sendmail(from_address, to_address, msg.as_string())
    s.close()


def send_verification_mail(user: User):
    import smtplib
    from email.mime.text import MIMEText

    from_address = current_app.config["EMAIL"]
    to_address = user.email

    msg = MIMEText(
        """Hi, {username}.
You have just registered to {ctf}. Please confirm your email address to access the following link.
{address}
    """.format(
            username=user.name,
            ctf=current_app.config["CTF_NAME"],
            address=os.path.join(request.url_root, "#/confirm/" + user.reset_token),
        )
    )
    msg["Subject"] = "{} registration confirm".format(current_app.config["CTF_NAME"])
    msg["From"] = from_address
    msg["To"] = to_address

    s = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    s.ehlo()
    s.login(from_address, current_app.config["EMAIL_PASSWORD"])
    s.sendmail(from_address, to_address, msg.as_string())
    s.close()


@user.route("/reset-request", methods=["POST"])
def resetRequest():
    username = request.json.get("username", "").strip()
    if not username:
        return error("Username is required")

    email = request.json.get("email", "").strip()
    if not email:
        return error("Email address is required")

    user = User.query.filter(User.name == username, User.email == email).first()
    if not user:
        return error("Username and/or email address is mismatching")

    if not user.verified:
        return error("Your email address is unverified")

    user.issueResetToken()
    db.session.add(user)
    db.session.commit()

    send_passwordreset_mail(user)
    return "", 204


@user.route("/reset", methods=["POST"])
def reset():
    token = request.json.get("token", "").strip()
    if not token:
        return error("The reset token is required")

    password = request.json.get("password", "").strip()
    if not password:
        return error("The password is required")

    user = User.query.filter(User.reset_token == token).first()
    if not user:
        return error("The token is invalid")

    if not user.checkToken(token):
        return error("The token is invalid or outdated")

    user.revokeToken()
    user.password = password
    db.session.add(user)
    db.session.commit()
    return "", 204


@user.route("/resend", methods=["POST"])
@login_required
def resend(user):
    email = request.json.get("email", "").strip()
    if not email:
        return error("Email address is required")

    if user.verified:
        return error("You are already verified")

    u2 = User.query.filter(User.email == email).first()
    if u2 and u2.id != user.id:
        return error("The email address is already used")

    user.email = email
    user.issueResetToken()
    db.session.add(user)
    db.session.commit()

    send_verification_mail(user)
    return "", 204


@user.route("/confirm", methods=["POST"])
def confirm():
    token = request.json.get("token", "").strip()
    if not token:
        return error("The token is required")

    user = User.query.filter(User.reset_token == token).first()
    if not user:
        return error("The token is invalid")

    if not user.checkToken(token):
        return error("The token is invalid or outdated")


    user.verified = True
    if not user.team.valid:
        user.team.valid = True
        user.team.renewToken()
    user.revokeToken()
    db.session.add(user)
    db.session.add(user.team)
    db.session.commit()

    return "", 204


@user.route("/register", methods=["POST"])
def register():
    if not Config.get().register_open:
        return error("Registration is closed")

    username = request.json.get("username", "").strip()
    if not username:
        return error("Username is required")
    user = User.query.filter(User.name == username).first()
    if user:
        return error("The user `{}` already exists".format(username))

    email = request.json.get("email", "").strip()
    if not email:
        return error("Email address is required")
    user = User.query.filter(User.email == email).first()
    if user:
        return error("The email address is already used")
    # TODO: check email format
    # TODO check the number of teammates

    password = request.json.get("password", "").strip()
    if not password:
        return error("Password is required")

    if request.json.get("teamtoken"):
        token = request.json.get("teamtoken").strip()
        team = Team.query.filter(Team.token == token, Team.valid == True).first()
        if not team:
            return error("The token is invalid")
    elif request.json.get("teamname"):
        teamname = request.json.get("teamname").strip()
        team = Team.query.filter(Team.name == teamname).first()
        if team and team.valid:
            return error("The team `{}` already exists".format(teamname))

        team = Team(name=teamname)
        team.valid = False
        db.session.add(team)
        db.session.commit()
    else:
        return error("Either team token or team name is required")

    user = User()
    user.name = username
    user.password = password
    user.email = email
    user.team_id = team.id
    user.verified = False
    user.issueResetToken()

    db.session.add(user)
    db.session.commit()

    send_verification_mail(user)

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
