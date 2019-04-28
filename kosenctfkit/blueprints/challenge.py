from flask import Blueprint, request, jsonify
from kosenctfkit.models import db, Config, Challenge, Submission, Team
from kosenctfkit.utils import error, login_required, ctf_open_required
from kosenctfkit.logging import logger

challenge = Blueprint("challenge", __name__)


@challenge.route("/submit", methods=["POST"])
@login_required
@ctf_open_required
def submit(user):
    challenge_id = request.json.get("id", None)
    if not challenge_id:
        return error("challenge id required")
    flag = request.json.get("flag", "").strip()
    if not challenge_id:
        return error("flag required")

    c = Challenge.query.filter(
        Challenge.id == challenge_id, Challenge.is_open == True
    ).first()
    if c is None:
        return error("invalid challenge id")

    if user.team:
        solves = user.team.getSolves(valid_only=False)
        team = user.team
    else:
        solves = user.getSolves(valid_only=False)
        team = Team()
        team.name = ""
    ids = [solved.id for solved in solves]
    already_solved = bool(c.id in ids)

    s = Submission()
    s.flag = flag
    s.challenge_id = c.id
    s.user_id = user.id
    if user.team:
        s.team_id = user.team.id

    if c.flag == flag and already_solved:
        logger.log(
            ":heavy_check_mark: `{}@{}` has submitted flag `{}` to `{}`. It has already solved.".format(
                user.name, team.name, c.name, flag
            )
        )
        return jsonify(
            {
                "message": "Correct, and you or your team already has solved `{}`".format(
                    c.name
                )
            }
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

        logger.log(
            ":heavy_check_mark: `{}@{}` has submitted flag `{}` to `{}`. :100:".format(
                user.name, team.name, c.name, flag
            )
        )
        return jsonify({"message": "Correct! You solved `{}`.".format(c.name)})

    elif c.flag != flag and already_solved:
        logger.log(
            ":x: `{}@{}` has submitted flag `{}` to `{}`. The correct flag is `{}`. This team already solved this challenges.".format(
                user.name, team.name, c.name, flag, c.flag
            )
        )
        return error(
            "Wrong flag, but you or your team already has solved `{}`".format(c.name)
        )

    else:
        s.is_valid = False
        s.is_correct = False

        db.session.add(s)
        db.session.commit()
        logger.log(
            ":x: `{}@{}` has submitted flag `{}` to `{}`. The correct flag is `{}`".format(
                user.name, team.name, c.name, flag, c.flag
            )
        )
        return error("Wrong flag")
