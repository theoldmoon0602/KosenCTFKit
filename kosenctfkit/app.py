from kosenctfkit.models import init_db
from kosenctfkit.logging import logger
from kosenctfkit.uploader import uploader
from kosenctfkit.blueprints import challenge, team, user, root


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
