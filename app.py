from flask import Flask, request, jsonify, session
from config import DefaultConfig
from kosenctfkit.models import db, init_db, Team, User

app = Flask(__name__, static_url_path="")


def error(message, status_code=400):
    res = jsonify(message=message)
    res.status_code = status_code
    return res


def login_required(f):
    from functools import wraps

    @wraps(f)
    def wrap(*args, **kwargs):
        user_id = session.get("user_id", None)
        if user_id is None:
            return error("Login required", 403)

        user = User.query.filter(User.id == user_id).first()
        if user is None:
            session.pop("user_id")
            return error("Login required", 403)

        kwargs["user"] = user
        return f(*args, **kwargs)

    return wrap


def userdump(user):
    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "team": user.team.name if user.team else None,
        },
        "team": {
            "id": user.team.id if user.team else None,
            "name": user.team.name if user.team else None,
            "members": [m.name for m in user.team.members] if user.team else None,
        },
    }


@app.route("/")
def root():
    return app.send_static_file("index.html")


@app.route("/register-team", methods=["POST"])
def register_team():
    teamname = request.json.get("teamname", None)
    if not teamname:
        return error("teamname is required")
    team = Team.query.filter(Team.name == teamname).first()
    if team and team.valid:
        return error("the team `{}` already exists".format(teamname))

    if not team:
        team = Team()
    team.name = teamname
    team.renewToken()
    db.session.add(team)
    db.session.commit()

    return jsonify({"id": team.id, "name": teamname, "token": team.token})


@app.route("/register", methods=["POST"])
def register():
    token = request.json.get("token", None)
    if not token:
        return error("token is required")

    username = request.json.get("username", None)
    if not username:
        return error("username is required")

    password = request.json.get("password", None)
    if not password:
        return error("password is required")

    team = Team.query.filter(Team.token == token).first()
    if not team:
        return error("the token is invalid")

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

    return jsonify({"id": user.id, "name": user.name})


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    if not username:
        return error("username is required")

    password = request.json.get("password", None)
    if not password:
        return error("password is required")

    user = User.query.filter(User.name == username).first()
    if not user:
        return error("user `{}` doesn't exist".format(username))

    if not user.check_password(password):
        return error("invalid password")

    session["user_id"] = user.id
    return jsonify(userdump(user))


@app.route("/logout")
def logout():
    _ = session.pop("user_id", None)
    return "", 204


@app.route("/me")
@login_required
def me(user):
    return jsonify(userdump(user))


if __name__ == "__main__":
    app.config.from_object(DefaultConfig)
    init_db(app)

    app.run()
