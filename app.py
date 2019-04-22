from flask import Flask, Blueprint
from config import DefaultConfig
from kosenctfkit.models import init_db

app = Flask(__name__, static_url_path="")


@app.route("/")
def root():
    return app.send_static_file("index.html")


@app.route("/register", methods=["POST"])
def register():
    pass


if __name__ == "__main__":
    app.config.from_object(DefaultConfig)
    init_db(app)

    app.run()
