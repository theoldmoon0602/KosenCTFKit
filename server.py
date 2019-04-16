import responder
import jwt
from asyncio import iscoroutinefunction
from kosenctfkit.app import App
from kosenctfkit.models import User
from config import ProductionConfig, DebugConfig
import os

config = ProductionConfig() if os.getenv('KOSENCTFKIT_PRODUCTION', None) else DebugConfig()
app = App(config)

api = responder.API(secret_key=app.config.SECRET_KEY, debug=app.config.DEBUG)
api.jinja_values_base['app'] = app

def login_required(f, arg_name='user', cookie_key='user'):
    def load_user(req, resp, *args, **kwargs):
        if cookie_key not in req.cookies:
            return None

        try:
            data = jwt.decode(req.cookies[cookie_key], api.secret_key, algorithms=['HS256'])
            return app.getUser(data['name'])
        except jwt.exceptions.InvalidTokenError:
            return None
        except KeyError:
            return None

    def not_authorized(req, resp, *args, **kwargs):
        resp.media = {"error": ["Login Required"]}
        resp.status_code = 403

    from functools import wraps
    if iscoroutinefunction(f):
        @wraps(f)
        async def login_f(*args, **kwargs):
            user = load_user(*args, **kwargs)
            if user:
                kwargs[arg_name] = user
                return f(*args, **kwargs)
            return not_authorized(*args, **kwargs)
        return login_f
    else:
        @wraps(f)
        def login_f(*args, **kwargs):
            user = load_user(*args, **kwargs)
            if user:
                kwargs[arg_name] = user
                return f(*args, **kwargs)
            return not_authorized(*args, **kwargs)
        return login_f

@api.route('/')
def index(req, resp):
    resp.html = api.template('base.html', base_url=api.url_for(index))

@api.route('/login')
class Login():
    async def on_post(self, req, resp):
        errors = []
        json = await req.media('json')

        username = json.get('username', '').strip()
        password = json.get('password', '').strip()

        if not username:
            errors.append('username is required')

        if not password:
            errors.append('password is required')

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
            resp.media = {
                "cookie-user": jwt.encode({"name": user.name}, api.secret_key, algorithm='HS256').decode('utf-8'),
                "user": {
                    "name": user.name,
                    "id": user.id,
                    "team": user.team.name if user.team else ''
                }
            }
        else:
            resp.media = {"error": ["incorrect password"]}
            resp.status_code = 400


@api.route('/me')
@login_required
def me(req, resp, *, user):
    resp.media = {
        "user": {
            "name": user.name,
            "id": user.id,
            "team": user.team.name if user.team else ''
        }
    }


@api.route('/register-team')
class RegisterTeam():
    async def on_post(self, req, resp):
        json = await req.media('json')

        teamname = json.get('teamname', '').strip()
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
            team = app.insertTeam({'name': teamname})

        resp.media = {"token": team.token}

@api.route('/register-user')
class RegisterUser():
    async def on_post(self, req, resp):
        errors = []
        json = await req.media('json')

        teamtoken = json.get('teamtoken', '').strip()
        username = json.get('username', '').strip()
        password = json.get('password', '').strip()
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

        user = app.makeUser({
            'name': username,
            'password': password,
        })
        try:
            app.joinTeam(user, teamtoken)
        except ValueError as e:
            resp.media = {"error": [str(e)]}
            resp.status_code = 400

@api.route('/myteam')
@login_required
def myteam(req, resp, *, user):
    team = user.team
    if team is None:
        resp.media = {"error": ["You are not in any team"]}
        resp.status_code = 400
        return
    resp.media = {
        'team': team.name,
        'token': team.token,
        'members': [{'name': m.name, 'id': m.id} for m in team.members.all()]
    }

@api.route('/regenerate')
@login_required
def regenerate(req, resp, *, user):
    team = user.team
    if team is None:
        resp.media = {"error": ["You are not in any team"]}
        resp.status_code = 400
        return

    team = app.renewTeamToken(team)
    resp.media = {
        'token': team.token,
    }

if __name__ == '__main__':
    api.run()
