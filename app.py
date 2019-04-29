from config import DefaultConfig
from kosenctfkit.app import init_app
from flask import Flask


if __name__ == "__main__":
    app = Flask(__name__, static_url_path="")
    init_app(app, DefaultConfig)
    app.run()
