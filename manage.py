import yaml
import time
import click
import tarfile
import os
import shutil
import subprocess
from pathlib import Path
from flask import Flask
from kosenctfkit.models import db, Config, User, Challenge, Attachment
from kosenctfkit.uploader import uploader
from kosenctfkit.app import init_app
from config import DefaultConfig

app = Flask(__name__)
init_app(app, DefaultConfig)


class Chall:
    def __init__(self, name, **kwargs):
        self.name = name
        self.category = kwargs["category"]
        self.base_score = kwargs["base_score"]
        self.author = kwargs["author"]
        self.testers = kwargs["testers"]
        self.description = kwargs["description"]
        self.completed = kwargs["completed"]
        self.flag = kwargs["flag"]
        self.column = None  # type: Challenge

    @property
    def normal_name(self) -> str:
        return self.name.replace(" ", "_").lower()

    def setChallenge(self, challenge: Challenge, expr):
        challenge.name = self.name
        challenge.category = self.category
        challenge.flag = self.flag
        challenge.description = self.description
        challenge.author = self.author
        challenge.testers = self.testers
        challenge.base_score = self.base_score
        challenge.is_open = challenge.is_open or False
        challenge.recalc_score(expr)

    def dump(self):
        buf = []

        buf.append("== {} ==".format(self.name))
        buf.append(" category  : {}".format(self.category))
        buf.append(" author    : {}".format(self.author))
        buf.append(" flag      : {}".format(self.flag))
        buf.append(" base_score: {}".format(self.base_score))
        buf.append(" testers   : {}".format(self.testers))
        buf.append(" completed : {}".format(self.completed))
        buf.append(" registered: {}".format(bool(self.column)))

        if self.column:
            buf.append("   open      : {}".format(self.column.is_open))
            buf.append("   solves    : {}".format(self.column.solve_num))
            buf.append("   score     : {}".format(self.column.score))
            buf.append(
                "   attachment: {}".format([a.url for a in self.column.attachments])
            )
        return "\n".join(buf)


class Challs:
    def __init__(self, cs, dirpath):
        self.dirpath = dirpath
        self.names = cs.keys()
        self.cs = {}
        for name, values in cs.items():
            self.cs[name] = Chall(name, **values)

    def list(self, all=False):
        for name in self.names:
            c = self.cs[name]
            if not all and not c.completed:
                continue
            c.column = Challenge.query.filter(Challenge.name == c.name).first()
            yield c

    def get(self, name):
        c = self.cs[name]
        c.column = Challenge.query.filter(Challenge.name == c.name).first()
        return c


def with_appcontext(f):
    from functools import wraps

    @wraps(f)
    def wrap(*args, **kwargs):
        with app.app_context():
            return f(*args, **kwargs)

    return wrap


def printConfig(config):
    from datetime import datetime

    start_at = datetime.fromtimestamp(config.start_at)
    end_at = datetime.fromtimestamp(config.end_at)

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
@click.argument("yaml_file", type=click.File("r"))
def init(yaml_file):
    """initialize CTF by yaml file"""
    ctf = yaml.safe_load(yaml_file)["ctf"]

    # check
    _ = int(eval(ctf["score_expr"], {"N": 0, "V": 1000}))

    # initialize db
    db.create_all()
    db.session.commit()

    # assign
    config = Config.get() or Config()  # type: Config
    config.name = ctf["name"]
    config.start_at = ctf["start_at"].timestamp()
    config.end_at = ctf["end_at"].timestamp()
    config.score_expr = ctf["score_expr"]
    config.is_open = config.is_open or False
    config.register_open = config.register_open or False

    admin = User.query.filter(User.is_admin == True).first() or User()  # type: User
    admin.name = ctf["admin"]["name"]
    admin.password = ctf["admin"]["password"]
    admin.is_admin = True

    # commit
    db.session.add(config)
    db.session.add(admin)
    db.session.commit()

    # print
    printConfig(config)
    print("[+]Done")


@cli.command()
@with_appcontext
def reset():
    """drop CTF database"""
    db.drop_all()
    print("[+]Done")


@cli.command()
@with_appcontext
@click.option("--only-register", is_flag=True)
def open(only_register):
    """open CTF and/or registration"""
    config = Config.get()
    config.register_open = True
    if not only_register:
        config.is_open = True

    # commit
    db.session.add(config)
    db.session.commit()

    # print
    printConfig(config)
    print("[+]Done")


@cli.command()
@with_appcontext
@click.option("--with-register", is_flag=True)
def close(with_register):
    """close CTF and/or registration"""
    config = Config.get()
    config.is_open = False
    if with_register:
        config.register_open = False

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
@click.pass_context
def challenge(ctx, directory):
    """manage challenges"""
    dirpath = Path(directory)
    yamlpath = dirpath / "challenges.yaml"
    if not yamlpath.exists():
        print("[-] file doesn't exist: {}".format(yamlpath))
        exit()

    with yamlpath.open() as f:
        challs = yaml.safe_load(f)["challenges"]
    ctx.ensure_object(dict)
    ctx.obj["dir"] = dirpath
    ctx.obj["challs"] = Challs(challs, dirpath)


@challenge.command("list")
@with_appcontext
@click.pass_context
@click.option("--all", is_flag=True)
def challenge_list(ctx, all):
    """list challenges"""
    for c in ctx.obj["challs"].list(all=all):
        print(c.dump())

    print("[+]Done")


@challenge.command("add")
@with_appcontext
@click.pass_context
@click.option("--only", help="challenge names to add separated with ,", default="")
def challenge_add(ctx, only):
    """add challenges to database"""
    only = [n for n in only.split(",") if n]

    config = Config.get()

    # commit
    for c in ctx.obj["challs"].list():  # type: Chall
        if only and c.name not in only:
            continue
        chall = c.column or Challenge()
        c.setChallenge(chall, config.score_expr)

        db.session.add(chall)
        db.session.commit()

        # delete current attachements
        chall.attachments.delete()
        db.session.commit()

        # archive attachement files
        distdir = ctx.obj["dir"] / c.normal_name / "distfiles"  # type: Path
        disttar = "{}.tar.gz".format(c.normal_name)
        if distdir.exists():
            # archive
            with tarfile.open(disttar, "w:gz") as tar:
                tar.add(distdir, arcname=c.normal_name)

            # upload
            path = uploader.upload_attachment(disttar)

            # remove
            os.remove(disttar)

            if not path:
                print("[-] failed to upload attachment")

            # save to database
            a = Attachment()
            a.challenge_id = chall.id
            a.url = path
            db.session.add(a)
            db.session.commit()

        # ditto
        distdir = ctx.obj["dir"] / c.normal_name / "distarchive"  # type: Path
        for distfile in distdir.glob("*"):
            path = uploader.upload_attachment(distfile)
            if not path:
                print("[-] failed to upload attachment")
                continue

            # save to database
            a = Attachment()
            a.challenge_id = chall.id
            a.url = path
            db.session.add(a)
            db.session.commit()

    # print
    for c in ctx.obj["challs"].list():  # type: Chall
        if only and c.name not in only:
            continue
        print(c.dump())
    print("[+]Done")


@challenge.command("open")
@with_appcontext
@click.pass_context
@click.option("--close", help="close instead to open", is_flag=True)
@click.option("--only", help="challenge names to open separated with ,", default="")
def challenge_open(ctx, only, close):
    """open challenges"""
    only = [n for n in only.split(",") if n]

    # commit
    for c in ctx.obj["challs"].list():  # type: Chall
        if only and c.name not in only:
            continue
        chall = c.column
        if chall is None:
            print("[-] {} is not in the Database".format(c.name))
            continue
        chall.is_open = not close
        db.session.add(chall)
        db.session.commit()

    # print
    for c in ctx.obj["challs"].list():  # type: Chall
        if only and c.name not in only:
            continue
        print(c.dump())
    print("[+]Done")


@challenge.command("recalc")
@with_appcontext
@click.pass_context
def challenge_recalc(ctx):
    """recalc challenge scores"""
    config = Config.get()  # type: Config

    # commit
    for c in ctx.obj["challs"].list():  # type: Chall
        chall = c.column
        if chall is None:
            continue
        chall.recalc_score(config.score_expr)

        db.session.add(chall)
        db.session.commit()

    # print
    for c in ctx.obj["challs"].list():  # type: Chall
        if c.column is None:
            continue
        print(c.dump())
    print("[+]Done")


def check_challenge(challenge, challenge_dir, workspace_name="workspace"):
    c = challenge
    workspace = Path(workspace_name)
    solutiondir = challenge_dir / c.normal_name / "solution"
    solutionscript = solutiondir / "solve.bash"
    distdir = challenge_dir / c.normal_name / "distfiles"
    distarchive_dir = challenge_dir / c.normal_name / "distarchive"

    if not solutiondir.exists():
        print("[-] no solution for the challenge: {}".format(c.name))
        exit(1)

    if not solutionscript.exists():
        print("[-] no solution script for the challenge: {}".format(c.name))
        exit(1)

    # create workspace
    shutil.copytree(solutiondir, workspace)

    # copy distributed files to solution directory
    if distdir.exists():
        for f in distdir.iterdir():
            if f.is_dir():
                shutil.copytree(f, workspace / f.name)
            else:
                shutil.copy(f, workspace)
    if distarchive_dir.exists():
        for f in distarchive_dir.glob("*.tar.gz"):
            with tarfile.open(f, "r:gz") as tar:
                tar.extractall(path=workspace)

    # run solver and check output
    try:
        env = dict(os.environ)
        host = app.config["CATEGORY_SERVERS"].get(c.category)
        if host:
            env.update({"CHALLENGE_HOST": host["host"]})
        result = subprocess.check_output(
            ["bash", "-c", "bash solve.bash"], cwd=workspace, env=env
        )
    except Exception as e:
        result = b""
        pass

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
@click.pass_context
def challenge_check(ctx, challenge):
    """run a check script for the challenge"""
    c = ctx.ob["challs"].get(challenge)
    if not c:
        print("[-] no such challenge")
        return
    r = check_challenge(c, ctx.obj["dir"])
    if r:
        print("[+] solved")
    else:
        print("[-] unsolved")
        exit(1)


@challenge.command("deploy")
@with_appcontext
@click.argument("challenge")
@click.option("--check", is_flag=True)
@click.pass_context
def challenge_deploy(ctx, challenge, check):
    """deploy challenge to remote"""

    # get chall
    c = ctx.obj["challs"].get(challenge)
    if not c:
        print("[-] no such challenge")
        return

    # check docker-compose.yaml
    challenge_dir = ctx.obj["dir"] / c.normal_name
    compose_file = challenge_dir / "docker-compose.yaml"
    if not compose_file.exists():
        print("[-] challenge dosn't have a docker-compose.yaml")
        return

    # check server settings
    server = app.config["CATEGORY_SERVERS"].get(c.category)
    if not server:
        print("[-] challenge category {} doesn't have a remote server setting")
        return

    # launch deploy commands
    try:
        subprocess.run(
            [
                "rsync",
                "-a",
                "-e",
                "ssh",
                challenge_dir,
                "{}:~".format(server["ssh_config"]),
            ]
        )
        subprocess.run(
            [
                "ssh",
                server["ssh_config"],
                "cd {}; docker-compose up --build -d".format(c.normal_name),
            ]
        )
    except subprocess.SubprocessError as e:
        print("[-] error on deplyoing")
        print(e)
        exit(1)

    print("[+] deploy done")
    if check:
        time.sleep(10)
        r = check_challenge(c, ctx.obj["dir"])
        if r:
            print("[+] solved")
        else:
            print("[+] unsolved")
            exit(1)


@challenge.command("stop")
@with_appcontext
@click.argument("challenge")
@click.pass_context
def challenge_deploy(ctx, challenge):
    """stop running challenge on remote"""

    # get chall
    c = ctx.obj["challs"].get(challenge)
    if not c:
        print("[-] no such challenge")
        return

    # check docker-compose.yaml
    challenge_dir = ctx.obj["dir"] / c.normal_name
    compose_file = challenge_dir / "docker-compose.yaml"
    if not compose_file.exists():
        print("[-] challenge dosn't have a docker-compose.yaml")
        return

    # check server settings
    server = app.config["CATEGORY_SERVERS"].get(c.category)
    if not server:
        print("[-] challenge category {} doesn't have a remote server setting")
        return

    # launch deploy commands
    try:
        subprocess.run(
            [
                "ssh",
                server["ssh_config"],
                "cd {}; docker-compose stop".format(c.normal_name),
            ]
        )
    except subprocess.SubprocessError as e:
        print("[-] error on stopping")
        print(e)
        exit(1)

    print("[+] done")


if __name__ == "__main__":
    cli()
