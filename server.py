import responder
from kosenctfkit.app import App
from kosenctfkit.apiutils import method_decorator, LoginManager
from config import ProductionConfig, DebugConfig
import os

config = (
    ProductionConfig() if os.getenv("KOSENCTFKIT_PRODUCTION", None) else DebugConfig()
)
app = App(config)

api = responder.API(secret_key=app.config.SECRET_KEY, debug=app.config.DEBUG)
api.jinja_values_base["app"] = app
lm = LoginManager(api, app)


@api.route("/")
def index(req, resp):
    resp.html = api.template("base.html", base_url=api.url_for(index))


@api.route("/login")
class Login:
    async def on_post(self, req, resp):
        errors = []
        json = await req.media("json")

        username = json.get("username", "").strip()
        password = json.get("password", "").strip()

        if not username:
            errors.append("username is required")

        if not password:
            errors.append("password is required")

        if errors:
            resp.media = {"error": errors}
            resp.status_code = 400
            return

        user = app.getUser(username)
        if user is None:
            resp.media = {"error": ["user `{}` doesn't exist".format(username)]}
            resp.status_code = 400
            return

        if user.check_password(password):
            lm.login(resp, user.name)
        else:
            resp.media = {"error": ["incorrect password"]}
            resp.status_code = 400


@api.route("/me")
@lm.login_required
def me(req, resp, *, user):
    resp.media = {
        "user": {
            "name": user.name,
            "score": app.userScore(user),
            "id": user.id,
            "team": user.team.name if user.team else "",
        }
    }


@api.route("/challenges")
@lm.login_required
def challenges(req, resp, *, user):
    if user.team:
        solves = [c.id for c in app.teamSolves(user.team)]
    else:
        solves = [c.id for c in app.userSolves(user)]

    cs = app.allChallenges(False)
    scores = app.challengeScores(cs)
    challenges = []
    for c in cs:
        challenges.append(
            {
                "id": c.id,
                "name": c.name,
                "score": scores[c.id],
                "description": c.description,
                "category": c.category,
                "author": c.author,
                "testers": c.testers.split(","),
                "solved": c.id in solves,
            }
        )
    resp.media = challenges


@api.route("/register-team")
class RegisterTeam:
    async def on_post(self, req, resp):
        json = await req.media("json")

        teamname = json.get("teamname", "").strip()
        if not teamname:
            resp.media = {"error": ["teamname is required"]}
            resp.status_code = 400
            return

        team = app.getTeam(teamname)
        if team and team.valid:
            resp.media = {"error": ["team `{}` already exists".format(team.name)]}
            resp.status_code = 400
            return

        if team:
            team = app.renewTeamToken(team)
        else:
            team = app.insertTeam({"name": teamname})

        resp.media = {"token": team.token}


@api.route("/register-user")
class RegisterUser:
    async def on_post(self, req, resp):
        errors = []
        json = await req.media("json")

        teamtoken = json.get("teamtoken", "").strip()
        username = json.get("username", "").strip()
        password = json.get("password", "").strip()
        if not teamtoken:
            errors.append("teamtoken is required")
        if not username:
            errors.append("username is required")
        if not password:
            errors.append("password is required")

        if errors:
            resp.media = {"error": errors}
            resp.status_code = 400
            return

        if app.getUser(username):
            resp.media = {"error": ["user `{}` already exists".format(username)]}
            resp.status_code = 400
            return

        user = app.makeUser({"name": username, "password": password})
        try:
            app.joinTeam(user, teamtoken)
        except ValueError as e:
            resp.media = {"error": [str(e)]}
            resp.status_code = 400


@api.route("/myteam")
@lm.login_required
def myteam(req, resp, *, user):
    team = user.team
    if team is None:
        resp.media = {"error": ["You are not in any team"]}
        resp.status_code = 400
        return

    resp.media = {
        "name": team.name,
        "score": app.teamScore(team),
        "token": team.token,
        "members": [{"name": m.name, "id": m.id} for m in team.members.all()],
    }


@api.route("/regenerate")
class Regenerate:
    @method_decorator(lm.login_required)
    def on_post(self, req, resp, *, user):
        team = user.team
        if team is None:
            resp.media = {"error": ["You are not in any team"]}
            resp.status_code = 400
            return

        team = app.renewTeamToken(team)
        resp.media = {"token": team.token}


@api.route("/set_password")
class SetPassword:
    @method_decorator(lm.login_required)
    async def on_post(self, req, resp, *, user):
        json = await req.media("json")

        new_password = json.get("new_password", "").strip()
        current_password = json.get("current_password", "").strip()

        if not new_password or not current_password:
            resp.media = {
                "error": ["New password and current password both are required"]
            }
            resp.status_code = 400
            return

        if not user.check_password(current_password):
            resp.media = {"error": ["current password is wrong"]}
            resp.status_code = 400
            return

        user.password = new_password
        app.session.add(user)
        app.session.commit()


@api.route("/submit")
class Submit:
    @method_decorator(lm.login_required)
    async def on_post(self, req, resp, *, user):
        json = await req.media("json")

        flag = json.get("flag", "").strip()
        challenge_id = json.get("challenge_id", "").strip()

        challenge = app.getChallengeById(challenge_id)
        if not challenge or challenge.hidden:
            resp.media = {"error": "No such challenges"}
            resp.status_code = 400
            return

        submission = app.insertSubmission(flag, user, challenge)

        if submission.valid:
            resp.media = {"status": "Correct!", "solved": True}
            return

        if submission.solved:
            resp.media = {
                "status": "Correct! But you or your team are already solved this challenge.",
                "solved": True,
            }
            return

        resp.media = {"status": "Wrong...", "solved": False}


@api.route("/scoreboard")
def scoreboard(req, resp):
    teamscores = app.allTeamScores()

    scores = teamscores.values()
    ranking = list(
        sorted(scores, key=lambda x: (x["score"], -x["last_submission"]), reverse=True)
    )

    rank = 1
    ranking[0]["rank"] = rank
    for i in range(1, len(ranking)):
        if not (
            ranking[i]["score"] == ranking[i - 1]["score"]
            and ranking[i]["last_submission"] == ranking[i - 1]["last_submission"]
        ):
            rank += 1
        ranking[i]["rank"] = rank

    resp.media = ranking


if __name__ == "__main__":
    api.run()
