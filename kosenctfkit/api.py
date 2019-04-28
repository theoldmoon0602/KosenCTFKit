from kosenctfkit.models import User, Team, Challenge


def get_user_and_team(user, valid_only):
    return (
        {
            "id": user.id,
            "name": user.name,
            "team": user.team.name if user.team else None,
            "team_id": user.team.id if user.team else None,
        },
        {
            "id": user.team.id if user.team else None,
            "name": user.team.name if user.team else None,
            "token": user.team.token if user.team else None,
        },
    )


def get_challenges():
    cs = Challenge.query.filter(Challenge.is_open == True).all()
    ret = {}

    for c in cs:
        ret[c.id] = {
            "id": c.id,
            "name": c.name,
            "category": c.category,
            "author": c.author,
            "testers": c.testers,
            "score": c.score,
            "solved": c.solve_num,
            "description": c.description,
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
            "icon": u.icon,
            "team": u.team.name if u.team else None,
            "team_id": u.team.id if u.team else None,
            "score": u.getScore(valid_only=valid_only),
            "solved": [c.id for c in u.getSolves(valid_only=valid_only)],
            "last_submission": u.last_submission,
        }
    return ret
