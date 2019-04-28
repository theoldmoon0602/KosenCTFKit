from flask import jsonify, session
from kosenctfkit.models import Config, User
from functools import wraps


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
