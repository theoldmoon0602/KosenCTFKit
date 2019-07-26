from flask import jsonify, session, url_for, current_app
from kosenctfkit.models import Config, User, Team, Challenge
from functools import wraps
import os.path


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


def ctf_open_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        config = Config.get()
        if not config.is_open:
            return error("CTF has been closed", 403)
        return f(*args, **kwargs)

    return wrap


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


def as_url(app, path):
    if not path:
        return path

    from urllib.parse import urlparse

    try:
        _ = urlparse(path)
        return path
    except ValueError:
        return url_for(
            "static",
            filename=os.path.join(
                app.static_url_path, os.path.relpath(path, app.static_folder)
            ),
        )


def get_user_and_team(user, valid_only):
    return (
        # user
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "verified": user.verified,
            "team": user.team.name if user.team else None,
            "team_id": user.team.id if user.team else None,
        },
        # team
        {
            "id": user.team.id if user.team else None,
            "name": user.team.name if user.team else None,
            "token": user.team.token if user.team else None,
        },
    )


def get_challenges(abst=False):
    cs = Challenge.query.filter(Challenge.is_open == True).all()
    ret = {}

    for c in cs:
        if abst:
            ret[c.id] = {"id": c.id, "name": c.name, "score": c.score}
        else:
            ret[c.id] = {
                "id": c.id,
                "name": c.name,
                "tags": c.tags,
                "author": c.author,
                "score": c.score,
                "solved": c.solve_count,
                "description": c.description.replace("{{host}}", c.host or "").replace(
                    "{{port}}", str(c.port or "")
                ),
                "attachments": [
                    as_url(current_app, a.url) for a in c.attachments.all()
                ],
                "difficulty": c.difficulty,
            }

    return ret


def get_teams(valid_only):
    ts = Team.query.filter(Team.valid == True).all()
    ret = {}
    for t in ts:
        ret[t.id] = {
            "id": t.id,
            "name": t.name,
            "members": [m.id for m in t.members.all()],
            "score": t.getScore(valid_only=valid_only),
            "solved": [c.id for c in t.getSolves(valid_only=valid_only)],
            "last_submission": t.last_submission,
        }
    return ret


def get_users(valid_only):
    us = User.query.filter(User.is_admin == False).all()
    ret = {}
    for u in us:
        ret[u.id] = {
            "id": u.id,
            "name": u.name,
            "icon": as_url(current_app, u.icon),
            "team": u.team.name if u.team else None,
            "team_id": u.team.id if u.team else None,
            "score": u.getScore(valid_only=valid_only),
            "solved": [c.id for c in u.getSolves(valid_only=valid_only)],
            "last_submission": u.last_submission,
        }
    return ret
