from kosenctfkit.models import db, init_db, Config, User, Challenge, Attachment
from kosenctfkit.app import init_app
from kosenctfkit.uploader import uploader
from config import DefaultConfig
from flask import Flask
import tarfile
import os
import shutil
import sys
import json
import pytz
from datetime import datetime

help = """\
manage.py COMMAND [options]

COMMAND
-------
init <ctfconfig.json>       --- Initialize Database with Config
reset                       --- Drop all tables
open-register               --- Open Registration
open-ctf                    --- Open CTF & Registration
close-register              --- Close Registration
close-ctf                   --- Close CTF & Registration
set-challenges <directory>  --- Set Challenges as Hidden
list-challenges             --- List Challenges
open-challenges [name]      --- Open Challenge by Name
recalc-challenges           --- Recalculate all Scores of Challenges
"""

if len(sys.argv) <= 1:
    print(help)
    exit()

app = Flask(__name__, static_url_path="")
init_app(app, DefaultConfig)


def normalize(f):
    return f.replace(" ", "_").lower()


def open_challenges(challenges):
    with app.app_context():
        if challenges:
            cs = Challenge.query.filter(Challenge.name.in_(challenges)).all()
        else:
            cs = Challenge.query.all()
        if len(cs) == 0:
            print("[-]Nothing to open")
            exit()
        for c in cs:
            c.is_open = True
            db.session.add(c)
            print("open {}".format(c.name))
        db.session.commit()
    print("[+]Done")


def list_challenges():
    with app.app_context():
        for c in Challenge.query.all():
            print("{} {}".format("o" if c.is_open else "x", c.name))


def set_challenges(directory):
    for p in os.listdir(directory):
        d = os.path.join(directory, p)
        if not os.path.isdir(d):
            continue

        jsonfile = os.path.join(d, "challenge.json")
        if not os.path.exists(jsonfile):
            continue

        with open(jsonfile) as jsonf:
            challenge_data = json.load(jsonf)

        name = challenge_data["name"]
        completed = challenge_data["completed"]
        base_score = challenge_data["base_score"]
        author = challenge_data["author"]
        testers = challenge_data["testers"]
        description = challenge_data["description"]
        flag = challenge_data["flag"]
        category = challenge_data["category"]

        # TODO: BUILD, ATTACHMENTS, DEPLOYMENT
        if not completed:
            continue

        n = normalize(name)
        disttar = "{}.tar.gz".format(n)
        distfiles = os.path.join(d, "distfiles")
        if os.path.isdir(distfiles):
            print("[+]archive attachments")
            with tarfile.open(disttar, "w:gz") as tar:
                tar.add(distfiles, arcname=n)

        with app.app_context():
            c = Challenge.query.filter(Challenge.name == name).first()
            if not c:
                c = Challenge()
            c.name = name
            c.is_open = False
            c.base_score = base_score
            c.score = eval(Config.get().score_expr, {"N": 0, "V": base_score})
            c.author = author
            c.testers = testers
            c.description = description
            c.flag = flag
            c.category = category

            db.session.add(c)
            db.session.commit()

            if os.path.exists(disttar):
                print("[+]upload attachment")
                path = uploader.upload_attachment(disttar)
                if path:
                    a = Attachment.query.filter(Attachment.url == path).first()
                    if not a:
                        a = Attachment()
                    a.challenge_id = c.id
                    a.url = path
                    db.session.add(a)
                    db.session.commit()
                print("[+]remove attachment")
                os.remove(disttar)

        print("[+]set {}".format(name))
    print("[+]Done")


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

        config = Config().get()
        if not config:
            config = Config()
        config.name = name
        config.start_at = start_at
        config.end_at = end_at
        config.score_expr = score_expr
        config.is_open = is_open
        config.register_open = register_open

        admin = User.query.filter(User.is_admin == True).first()
        if not admin:
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

elif sys.argv[1] == "open-register":
    with app.app_context():
        config = Config.get()
        config.register_open = True
        db.session.add(config)
        db.session.commit()
    print("[+]Done")

elif sys.argv[1] == "open-ctf":
    with app.app_context():
        config = Config.get()
        config.register_open = True
        config.is_open = True
        db.session.add(config)
        db.session.commit()
    print("[+]Done")

elif sys.argv[1] == "close-register":
    with app.app_context():
        config = Config.get()
        config.register_open = False
        db.session.add(config)
        db.session.commit()
    print("[+]Done")

elif sys.argv[1] == "close-ctf":
    with app.app_context():
        config = Config.get()
        config.register_open = False
        config.is_open = False
        db.session.add(config)
        db.session.commit()
    print("[+]Done")

elif sys.argv[1] == "open-challenges":
    open_challenges(sys.argv[2:])

elif sys.argv[1] == "list-challenges":
    list_challenges()

elif sys.argv[1] == "set-challenges":
    if len(sys.argv) <= 2:
        print(help)
        exit()
    set_challenges(sys.argv[2])

elif sys.argv[1] == "recalc-challenges":
    with app.app_context():
        conf = Config.get()
        cs = Challenge.query.filter(Challenge.is_open == True).all()
        for c in cs:
            c.recalc_score(conf.score_expr)
            db.session.add(c)
            print("[+]Recalculated {}".format(c.name))
        db.session.commit()
    print("[+]Done")

elif sys.argv[1] == "reset":
    with app.app_context():
        db.drop_all()
    print("[+]Done")

else:
    print(help)
