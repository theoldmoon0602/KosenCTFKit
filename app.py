from flask import Flask, request, jsonify, session
from config import DefaultConfig
from kosenctfkit.models import db, init_db, Team, User, Config, Challenge, Submission
from functools import wraps

app = Flask(__name__, static_url_path="")


def error(message, status_code=400):
    res = jsonify(message=message)
    res.status_code = status_code
    return res


def get_login_user():
    user_id = session.get("user_id", None)
    if user_id is None:
        return None
    user = User.query.filter(User.id == user_id).first()
    return user


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user = get_login_user()
        if user is None:
            session.pop("user_id", None)
            return error("Login required", 403)

        kwargs["user"] = user
        return f(*args, **kwargs)

    return wrap


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
    return jsonify(user_info(user)[0])


@app.route("/logout")
def logout():
    _ = session.pop("user_id", None)
    return "", 204


@app.route("/update")
def update():
    user = get_login_user()
    config = Config.get()
    ctf_open = config.ctf_open
    ctf_frozen = config.ctf_frozen
    if user is None:
        return jsonify(
            {"is_login": False, "ctf_open": ctf_open, "ctf_frozen": ctf_frozen}
        )
    else:
        userinfo, teaminfo = user_info(user, valid_only=(not ctf_frozen))
        return jsonify(
            {
                "is_login": True,
                "ctf_open": ctf_open,
                "ctf_frozen": ctf_frozen,
                "user": userinfo,
                "team": teaminfo,
                "challenges": challenge_info(),
            }
        )


def user_info(user, valid_only):
    return (
        {
            "id": user.id,
            "name": user.name,
            "team": user.team.name if user.team else None,
            "score": user.getScore(valid_only=valid_only),
            "solved": [c.id for c in user.getSolves(valid_only=valid_only)],
        },
        {
            "id": user.team.id if user.team else None,
            "name": user.team.name if user.team else None,
            "token": user.team.token if user.team else None,
            "members": [m.name for m in user.team.members] if user.team else [],
            "score": user.team.getScore(valid_only=valid_only)
            if user.team
            else user.getScore(valid_only=valid_only),
            "solved": [
                c.id
                for c in (
                    user.team.getSolves(valid_only=valid_only)
                    if user.team
                    else user.getSolves(valid_only=valid_only)
                )
            ],
        },
    )


def challenge_info():
    cs = Challenge.query.filter(Challenge.is_open == True).all()
    ret = []

    for c in cs:
        ret.append(
            {
                "id": c.id,
                "name": c.name,
                "category": c.category,
                "author": c.author,
                "testers": c.testers,
                "score": c.score,
                "solved": c.solves,
                "description": c.description,
            }
        )
    return ret


@app.route("/submit", methods=["POST"])
@login_required
def submit(user):
    challenge_id = request.json.get("id", None)
    if not challenge_id:
        return error("challenge id required")
    flag = request.json.get("flag", None)
    if not challenge_id:
        return error("flag required")

    c = Challenge.query.filter(
        Challenge.id == challenge_id, Challenge.is_open == True
    ).first()
    if c is None:
        return error("invalid challenge id")

    if user.team:
        solves = user.team.getSolves(valid_only=True)
    else:
        solves = user.getSolves(valid_only=True)
    ids = [solved.id for solved in solves]
    already_solved = bool(c.id in ids)

    s = Submission()
    s.flag = flag
    s.challenge_id = c.id
    s.user_id = user.id
    if user.team:
        s.team_id = user.team.id

    if c.flag == flag and already_solved:
        return jsonify(
            {
                "message": "Correct, and you or your team already has solved `{}`".format(
                    c.name
                )
            }
        )
    elif c.flag != flag and already_solved:
        return error(
            "Wrong flag, but you or your team already has solved `{}`".format(c.name)
        )

    elif c.flag == flag and not already_solved:
        s.is_valid = True
        s.is_correct = True

        db.session.add(s)
        db.session.commit()

        c.recalc_score(Config.get().score_expr)

        db.session.add(c)
        db.session.commit()
        return jsonify({"message": "Correct! You solved `{}`.".format(c.name)})

    else:
        s.is_valid = False
        s.is_correct = False

        db.session.add(s)
        db.session.commit()
        return error("Wrong flag")


if __name__ == "__main__":
    app.config.from_object(DefaultConfig)
    init_db(app)

    app.run()
