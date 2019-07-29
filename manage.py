import click
import yaml
import tarfile
import os
import shutil
import subprocess
import pytz
from pathlib import Path
from flask import Flask
from kosenctfkit.app import init_app
from kosenctfkit.models import User, Config, Challenge, Attachment, db
from config import config

app = Flask(__name__)
init_app(app, config)
challenges_dir = None
challenges = None


def normal_name(challenge_name):
    return challenge_name.replace(" ", "_").lower()


def with_appcontext(f):
    from functools import wraps

    @wraps(f)
    def wrap(*args, **kwargs):
        with app.app_context():
            return f(*args, **kwargs)

    return wrap


def printConfig(config):
    from datetime import datetime

    start_at = datetime.utcfromtimestamp(config.start_at)
    end_at = datetime.utcfromtimestamp(config.end_at)

    status = "closed"
    if config.register_open:
        status = "register_open"
    if config.ctf_frozen:
        status = "frozen"
    if config.ctf_open:
        status = "running"

    print("=== {} ===".format(config.name))
    print(" hold between (UTC): {} - {}".format(start_at, end_at))
    print(" is open           : {}".format(config.is_open))
    print(" register open     : {}".format(config.register_open))
    print(" current status    : {}".format(status))


@click.group()
def cli():
    pass


@cli.command()
@with_appcontext
def init():
    """initialize CTF by yaml file"""
    # initialize db
    db.create_all()
    db.session.commit()

    ctf = Config.get() or Config()  # type: Config
    ctf.name = app.config["CTF_NAME"]
    ctf.flag_format = app.config["FLAGFORMAT"]
    ctf.start_at = int(
        app.config["START_AT"].timestamp()
        - app.config["START_AT"].utcoffset().total_seconds()
    )
    ctf.end_at = int(
        app.config["END_AT"].timestamp()
        - app.config["END_AT"].utcoffset().total_seconds()
    )
    ctf.score_expr = app.config["SCORE_EXPR"]
    ctf.is_open = ctf.is_open or False
    ctf.register_open = ctf.register_open or False

    admin = User.query.filter(User.is_admin == True).first() or User()  # type: User
    admin.name = app.config["ADMIN_NAME"]
    admin.email = "admin@example.com"
    admin.verified = True
    admin.password = app.config["ADMIN_PASSWORD"]
    admin.is_admin = True

    # commit
    db.session.add(ctf)
    db.session.add(admin)
    db.session.commit()

    # print
    printConfig(ctf)


@cli.command()
@with_appcontext
def reset():
    """drop CTF database"""
    db.drop_all()
    print("[+]Done")


@cli.command()
@with_appcontext
@click.option("--register", is_flag=True, help="open/close only registration")
@click.option("--close", is_flag=True, help="close instead of opening")
def open(register, close):
    """open CTF and/or registration"""
    config = Config.get()
    config.register_open = not close
    if not register:
        config.is_open = not close

    # commit
    db.session.add(config)
    db.session.commit()

    # print
    printConfig(config)
    print("[+]Done")


@cli.group()
@click.option(
    "-d",
    "--directory",
    help="directory at challenges.yaml",
    required="True",
    default="challenges",
)
def challenge(directory):
    """manage challenges"""
    global challenges_dir, challenges
    challenges_dir = Path(directory)
    yamlpath = challenges_dir / "challenges.yaml"
    if not yamlpath.exists():
        print("[-] file doesn't exist: {}".format(yamlpath))
        exit()

    with yamlpath.open() as f:
        challenges = yaml.safe_load(f)["challenges"]

    for name in challenges.keys():
        if challenges[name].get("completed", True) is False:
            continue
        challenges[name]["name"] = name


@challenge.command("list")
@with_appcontext
def challenge_list():
    """list challenges"""
    challs = {c.name: c for c in Challenge.query.all()}
    for name, _ in challenges.items():
        if name not in challs:
            print("[+]UNREGISTERED {}".format(name))
        elif challs[name].is_open:
            print("[+]OPENED       {}".format(name))
        else:
            print("[+]CLOSED       {}".format(name))


@challenge.command("add")
@with_appcontext
@click.argument("names", nargs=-1)
@click.option("--all", help="add all challenges", is_flag=True)
def challenge_add(names, all):
    """add challenges to database"""

    for name, c in challenges.items():  # type: Chall
        # filter
        if not all and name not in names:
            continue

        if c.get("completed", True) is False:
            continue

        chall = Challenge.query.filter(Challenge.name == name).first() or Challenge()
        chall.name = name
        chall.flag = c["flag"]
        chall.description = c["description"]
        chall.tags = c["tags"]
        chall.difficulty = c["difficulty"]
        chall.author = c["author"]
        chall.base_score = c["base_score"]
        chall.score = chall.score or c["base_score"]
        chall.host = c.get("host")
        chall.port = c.get("port")

        db.session.add(chall)
        db.session.commit()
        print("[+]ADD {}".format(chall.name))

        # delete current attachements
        chall.attachments.delete()
        db.session.commit()

        # search attachment
        distfiles = challenges_dir / normal_name(chall.name) / "distfiles"
        tar_name = "{}.tar.gz".format(normal_name(chall.name))
        if distfiles.exists():
            # archive
            with tarfile.open(tar_name, "w:gz") as tar:
                tar.add(distfiles, arcname=normal_name(chall.name))

            # upload && remove
            url = app.uploader.upload_attachment(tar_name)
            os.remove(tar_name)

            # add attachments to challenge
            attachment = Attachment(url=url, challenge_id=chall.id)
            db.session.add(attachment)
            db.session.commit()
            print("  Attachment {}".format(tar_name))

        distarchive = challenges_dir / normal_name(chall.name) / "distarchive"
        if distarchive.exists():
            for tar_name in os.listdir(distarchive):
                url = app.uploader.upload_attachment(distarchive / tar_name)
                attachment = Attachment(url=url, challenge_id=chall.id)
                db.session.add(attachment)
                db.session.commit()
                print("  Attachment {}".format(tar_name))


@challenge.command("open")
@with_appcontext
@click.argument("names", nargs=-1)
@click.option("--all", help="open all challenges", is_flag=True)
@click.option("--close", help="close instead to open", is_flag=True)
def challenge_open(names, all, close):
    """open challenges"""
    # commit
    for name, _ in challenges.items():
        if not all and name not in names:
            continue

        chall = Challenge.query.filter(Challenge.name == name).first()
        if not chall:
            continue

        chall.is_open = not close
        db.session.add(chall)
        db.session.commit()

        print("[+]{} {}".format(["OPENED", "CLOSED"][int(close)], chall.name))


@challenge.command("recalc")
@with_appcontext
def challenge_recalc():
    """recalc challenge scores"""
    config = Config.get()  # type: Config

    # commit
    for chall in Challenge.query.all():  # type: Chall
        chall.recalc_score(config.score_expr)

        db.session.add(chall)
        db.session.commit()
        print("[+]{}: {}".format(chall.score, chall.name))


def check_challenge(challenge, workspace_name="workspace"):
    workspace = Path(workspace_name)
    challengedir = challenges_dir / normal_name(challenge["name"])
    solutiondir = challengedir / "solution"
    solutionscript = solutiondir / "solve.sh"
    distfiles = challengedir / "distfiles"
    distarchive = challengedir / "distarchive"

    if not solutiondir.exists():
        print("[-] no solution for the challenge: {}".format(challenge["name"]))
        exit(1)

    if not solutionscript.exists():
        print("[-] no solution script for the challenge: {}".format(challenge["name"]))
        exit(1)

    # create workspace
    shutil.copytree(solutiondir, workspace)

    # copy distributed files to solution directory
    if distfiles.is_dir():
        for f in distfiles.iterdir():
            if f.is_dir():
                shutil.copytree(f, workspace / f.name)
            else:
                shutil.copy(f, workspace)
    if distarchive.is_dir():
        for f in distarchive.glob("*.tar.gz"):
            with tarfile.open(f, "r:gz") as tar:
                tar.extractall(path=workspace)

    # run solver and check output
    try:
        env = dict(os.environ)
        if challenge.get("host"):
            env.update({"HOST": challenge.get("host")})
        if challenge.get("port"):
            env.update({"PORT": str(challenge.get("port"))})

        result = subprocess.check_output(["sh", "solve.sh"], cwd=workspace, env=env)
    except Exception as e:
        print("[-] {}".format(str(e)))
        result = b""

    # remove workspace
    shutil.rmtree(workspace)

    # check if the challenge is solved
    if c.flag.encode() in result:
        return True
    else:
        return False


@challenge.command("check")
@with_appcontext
@click.argument("challenge")
def challenge_check(challenge):
    """run a check script for the challenge"""
    if challenge not in challenges:
        print("[-] no such challenge")
        return

    r = check_challenge(challenges[challenge])
    if r:
        print("[+] solved")
    else:
        print("[-] unsolved")
        exit(1)


@challenge.command("deploy")
@with_appcontext
@click.argument("challenge")
def challenge_deploy(challenge):
    """deploy challenge to remote"""
    # get chall
    challenge = challenges.get(challenge)
    if challenge is None:
        print("[-] no such challenge")
        return

    # check docker-compose.yaml
    challengedir = challenges_dir / normal_name(challenge["name"])
    docker_compose = challengedir / "docker-compose.yaml"
    if not docker_compose.exists():
        docker_compose = challengedir / "docker-compose.yml"
        if not docker_compose.exists():
            print("[-] challenge dosn't have a docker-compose.ya?ml")
            return

    # check server settings
    if challenge.get("host") is None:
        print("[-] no host deply to")
        return

    # launch deploy commands
    ssh_config = app.config["SSH"][challenge["host"]]
    try:
        subprocess.run(
            ["rsync", "-a", "-e", "ssh", challengedir, "{}:/tmp/".format(ssh_config)]
        )
        subprocess.run(
            [
                "ssh",
                ssh_config,
                "cd /tmp/{}; env PORT={} docker-compose up --build -d".format(
                    normal_name(challenge["name"]), challenge["port"]
                ),
            ]
        )
    except subprocess.SubprocessError as e:
        print("[-] error on deplyoing: {}".format(e))
        exit(1)

    print("[+] deploy done")


@challenge.command("stop")
@with_appcontext
@click.argument("challenge")
def challenge_stop(challenge):
    """stop running challenge on remote"""
    # get chall
    challenge = challenges.get(challenge)
    if challenge is None:
        print("[-] no such challenge")
        return

    # check docker-compose.yaml
    challengedir = challenges_dir / normal_name(challenge["name"])
    docker_compose = challengedir / "docker-compose.yaml"
    if not docker_compose.exists():
        docker_compose = challengedir / "docker-compose.yml"
        if not docker_compose.exists():
            print("[-] challenge dosn't have a docker-compose.ya?ml")
            return

    # check server settings
    if challenge.get("host") is None:
        print("[-] no host ")
        return

    # launch deploy commands
    ssh_config = app.config["SSH"][challenge["host"]]
    try:
        subprocess.run(
            [
                "ssh",
                ssh_config,
                "cd /tmp/{}; env PORT={} docker-compose stop".format(
                    normal_name(challenge["name"]), challenge["port"]
                ),
            ]
        )
    except subprocess.SubprocessError as e:
        print("[-] error on stopping: {}".format(e))
        exit(1)

    print("[+] stopped")


if __name__ == "__main__":
    cli()
