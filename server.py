import responder
from kosenctfkit.app import App
from kosenctfkit.models import User
from config import ProductionConfig, DebugConfig
import os

from responder_login import LoginManager

config = ProductionConfig() if os.getenv('KOSENCTFKIT_PRODUCTION', None) else DebugConfig()
app = App(config)

api = responder.API(secret_key=app.config.SECRET_KEY)
login_manager = LoginManager(api)
api.jinja_values_base['app'] = app

@login_manager.user_loader
def user_loader(user_id):
    return app.session.query(User).filter(User.id == user_id).first()


@api.route('/')
def index(req, resp):
    resp.html = api.template('base.html')

if __name__ == '__main__':
    api.run()
