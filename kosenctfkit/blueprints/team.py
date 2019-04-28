from flask import Blueprint, request, jsonify
from kosenctfkit.models import db, Config, Team
from kosenctfkit.utils import error, login_required


team = Blueprint("team", __name__)


@team.route("/register", methods=["POST"])
def register():
    teamname = request.json.get("teamname", None)
    if not teamname:
        return error("teamname is required")

    if not Config.get().register_open:
        return error("Registration is closed")

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


@team.route("/regenerate", methods=["POST"])
@login_required
def regenerate(user):
    if user.team:
        user.team.renewToken()
        db.session.add(user.team)
        db.session.commit()
    return "", 204
