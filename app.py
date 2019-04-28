from flask import Flask, jsonify
from config import DefaultConfig
from kosenctfkit.models import init_db, Config
from kosenctfkit.logging import logger
from kosenctfkit.utils import get_login_user
from kosenctfkit.api import get_challenges, get_users, get_teams, get_user_and_team
from kosenctfkit.blueprints import challenge, team, user

app = Flask(__name__, static_url_path="")
app.register_blueprint(challenge)
app.register_blueprint(team)
app.register_blueprint(user)


@app.route("/")
def root():
    return app.send_static_file("index.html")


@app.route("/update")
def update():
    user = get_login_user()
    config = Config.get()
    ctf_name = config.name
    register_open = config.register_open
    ctf_open = config.ctf_open
    ctf_frozen = config.ctf_frozen
    valid_only = not ctf_frozen
    users = get_users(valid_only=valid_only)
    teams = get_teams(valid_only=valid_only)
    scoreboard = get_teams(valid_only=True)

    r = {
        "is_login": bool(user),
        "ctf_name": ctf_name,
        "ctf_open": ctf_open,
        "ctf_frozen": ctf_frozen,
        "register_open": register_open,
        "users": users,
        "teams": teams,
        "scoreboard": scoreboard,
        "challenges": {},
    }
    if user:
        userinfo, teaminfo = get_user_and_team(user, valid_only=valid_only)
        r["challenges"] = get_challenges()
        r["user"] = userinfo
        r["team"] = teaminfo
    return jsonify(r)


if __name__ == "__main__":
    app.config.from_object(DefaultConfig)
    init_db(app)
    if "WEBHOOK_URL" in app.config:
        logger.init(app.config["WEBHOOK_URL"])

    app.run()
