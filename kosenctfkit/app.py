from kosenctfkit.models import init_db
from kosenctfkit.logging import logger
from kosenctfkit.uploader import uploader
from kosenctfkit.blueprints import challenge, team, user, root
from kosenctfkit.utils import get_login_user
from kosenctfkit.models import (
    db,
    User,
    Team,
    Challenge,
    Submission,
    Attachment,
    Config,
    Log,
)
from flask import redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


class BaseModelView(ModelView):
    def is_accessible(self):
        user = get_login_user()
        if user:
            return user.is_admin
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("index"))


def init_app(app, config):
    app.config.from_object(config)

    app.register_blueprint(challenge)
    app.register_blueprint(team)
    app.register_blueprint(user)
    app.register_blueprint(root)

    def index():
        return app.send_static_file("index.html")

    app.add_url_rule("/", "index", index)

    init_db(app)
    if "WEBHOOK_URL" in app.config:
        logger.init(app.config["WEBHOOK_URL"])
    uploader.init(app)
    app.uploader = uploader

    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
    admin = Admin(app, name="admin", template_mode="bootstrap3")

    admin.add_view(BaseModelView(User, db.session))
    admin.add_view(BaseModelView(Team, db.session))
    admin.add_view(BaseModelView(Challenge, db.session))
    admin.add_view(BaseModelView(Submission, db.session))
    admin.add_view(BaseModelView(Attachment, db.session))
    admin.add_view(BaseModelView(Config, db.session))
    admin.add_view(BaseModelView(Log, db.session))
