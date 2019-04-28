from flask import Blueprint, request, jsonify, session
from kosenctfkit.models import db, Config, Team, User, Challenge, Submission
from kosenctfkit.utils import error, login_required, ctf_open_required

challenge = Blueprint("challenge", __name__)


@challenge.route("/submit", methods=["POST"])
@login_required
@ctf_open_required
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
        solves = user.team.getSolves(valid_only=False)
    else:
        solves = user.getSolves(valid_only=False)
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
        config = Config.get()
        if not config.ctf_frozen:
            s.is_valid = True
            s.is_correct = True
            db.session.add(s)
            db.session.commit()

            c.recalc_score(config.score_expr)
            db.session.add(c)
            db.session.commit()
        else:
            s.is_valid = False
            s.is_correct = True

            db.session.add(s)
            db.session.commit()

        return jsonify({"message": "Correct! You solved `{}`.".format(c.name)})

    else:
        s.is_valid = False
        s.is_correct = False

        db.session.add(s)
        db.session.commit()
        return error("Wrong flag")
