from flask import Flask, request, jsonify
from config import DefaultConfig
from kosenctfkit.models import db, init_db, Team

app = Flask(__name__, static_url_path="")


def error(message, status_code=400):
    res = jsonify(message=message)
    res.status_code = status_code
    return res


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
    pass


if __name__ == "__main__":
    app.config.from_object(DefaultConfig)
    init_db(app)

    app.run()
