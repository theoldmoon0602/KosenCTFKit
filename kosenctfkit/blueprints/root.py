from flask import Blueprint, jsonify
from kosenctfkit.models import Config, Submission
from kosenctfkit.utils import (
    login_required,
    get_login_user,
    get_users,
    get_teams,
    get_challenges,
    get_user_and_team,
)
from datetime import datetime


root = Blueprint("root_", __name__)


@root.route("/submissions")
def submissions():
    ret = []
    for s in Submission.query.filter(Submission.is_valid == True).all():
        ret.append(
            {
                "challenge_id": s.challenge_id,
                "user_id": s.user_id,
                "team_id": s.team_id,
                "created_at": s.created_at,
                "timestring": datetime.fromtimestamp(s.created_at).isoformat() + "Z",
            }
        )
    return jsonify(ret)


@root.route("/update")
def update():
    user = get_login_user()
    config = Config.get()
    ctf_name = config.name
    register_open = config.register_open
    ctf_open = config.ctf_open
    ctf_frozen = config.ctf_frozen
    valid_only = not ctf_frozen
    users = get_users(valid_only=valid_only)
    teams = get_teams(valid_only=True)

    r = {
        "is_login": bool(user),
        "start_at": datetime.fromtimestamp(config.start_at).isoformat() + "Z",
        "end_at": datetime.fromtimestamp(config.end_at).isoformat() + "Z",
        "ctf_name": ctf_name,
        "flag_format": config.flag_format,
        "invite_url": config.invite_url,
        "ctf_open": ctf_open,
        "ctf_frozen": ctf_frozen,
        "score_expr": config.score_expr.replace("V", "base_score").replace(
            "N", "solve_count"
        ),
        "register_open": register_open,
        "users": users,
        "teams": teams,
        "challenges": {},
    }
    if user:
        userinfo, teaminfo = get_user_and_team(user, valid_only=valid_only)
        r["user"] = userinfo
        r["team"] = teaminfo
    if config.ctf_open or config.ctf_frozen:
        r["challenges"] = get_challenges(abst=not bool(user))
    return jsonify(r)
