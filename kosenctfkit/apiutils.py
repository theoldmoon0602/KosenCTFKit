from asyncio import iscoroutinefunction
from functools import wraps
import jwt


def method_decorator(decorator):
    def new_decorator(f):
        if iscoroutinefunction(f):
            async def wrap(self, *args, **kwargs):
                @decorator
                async def without_self(*args2, **kwargs2):
                    return await f(self, *args2, **kwargs2)
                return await without_self(*args, **kwargs)
            return wrap

        else:
            def wrap(self, *args, **kwargs):
                @decorator
                def without_self(*args2, **kwargs2):
                    return f(self, *args2, **kwargs2)
                return without_self(*args, **kwargs)
            return wrap
    return new_decorator


class LoginManager():
    def __init__(self, api, app, arg_name='user', cookie_name='user', cookie_key='user-cookie'):
        self.api = api
        self.app = app
        self.arg_name = arg_name
        self.cookie_name = cookie_name
        self.cookie_key = cookie_key

    def login_required(self, f):
        def load_user(req, resp, *args, **kwargs):
            if self.cookie_name not in req.cookies:
                return None

            try:
                data = jwt.decode(req.cookies[self.cookie_name], self.api.secret_key, algorithms=['HS256'])
                return self.app.getUser(data['name'])
            except jwt.exceptions.InvalidTokenError:
                return None
            except KeyError:
                return None

        def not_authorized(req, resp, *args, **kwargs):
            resp.media = {"error": ["Login Required"]}
            resp.status_code = 403

        if iscoroutinefunction(f):
            @wraps(f)
            async def login_f(*args, **kwargs):
                user = load_user(*args, **kwargs)

                if user:
                    kwargs[self.arg_name] = user
                    return await f(*args, **kwargs)
                return not_authorized(*args, **kwargs)
            return login_f

        else:
            @wraps(f)
            def login_f(*args, **kwargs):
                user = load_user(*args, **kwargs)

                if user:
                    kwargs[self.arg_name] = user
                    return f(*args, **kwargs)
                return not_authorized(*args, **kwargs)
            return login_f

    def login(self, resp, name):
        resp.media = {
            self.cookie_key: jwt.encode({"name": name}, self.api.secret_key, algorithm='HS256').decode('utf-8'),
        }

