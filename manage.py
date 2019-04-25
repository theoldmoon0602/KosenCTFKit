from kosenctfkit.models import db, init_db, Config, User
from config import DefaultConfig
from flask import Flask
import sys
import json
import pytz
from datetime import datetime

help = """\
manage.py COMMAND [options]

COMMAND
-------
init <ctfconfig.json>   --- Initialize Database with Config
reset                   --- Drop all tables
"""

if len(sys.argv) <= 1:
    print(help)
    exit()

app = Flask(__name__, static_url_path="")
app.config.from_object(DefaultConfig)
init_db(app)


def init(conf):
    with open(conf) as f:
        ctf_conf = json.load(f)

    name = ctf_conf["name"]
    timezone = pytz.timezone(ctf_conf["timezone"])
    start_at = timezone.localize(
        datetime.strptime(ctf_conf["start_at"], "%Y-%m-%d %H:%M:%S")
    ).timestamp()
    end_at = timezone.localize(
        datetime.strptime(ctf_conf["end_at"], "%Y-%m-%d %H:%M:%S")
    ).timestamp()
    score_expr = ctf_conf["score_expr"]
    is_open = ctf_conf.get("is_open", False)
    register_open = ctf_conf.get("register_open", False)

    admin_username = ctf_conf["admin"]["name"]
    admin_password = ctf_conf["admin"]["password"]

    # check score_expr
    eval(score_expr, {"V": 1000, "N": 0})

    with app.app_context():
        db.create_all()

        config = Config()
        config.name = name
        config.start_at = start_at
        config.end_at = end_at
        config.score_expr = score_expr
        config.is_open = is_open
        config.register_open = register_open

        admin = User()
        admin.name = admin_username
        admin.password = admin_password
        admin.is_admin = True

        db.session.add(config)
        db.session.add(admin)
        db.session.commit()

    print("[+]Done")


if sys.argv[1] == "init":
    if len(sys.argv) <= 2:
        print(help)
        exit()
    init(sys.argv[2])


if sys.argv[1] == "reset":
    with app.app_context():
        db.drop_all()
    print("[+]Done")
