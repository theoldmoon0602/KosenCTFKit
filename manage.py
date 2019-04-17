from kosenctfkit.app import App
import yaml
import click
import os
import pytz
from datetime import datetime
from config import DebugConfig, ProductionConfig


@click.group()
@click.pass_context
def cli(ctx):
    config = ProductionConfig() if os.getenv('KOSENCTFKIT_PRODUCTION', None) else DebugConfig()
    app = App(config)

    ctx.ensure_object(dict)
    ctx.obj['app'] = app

@cli.command()
@click.pass_context
def reset(ctx):
    ctx.obj['app'].reset()
    print("[+]Done")


@cli.command()
@click.argument("conf")
@click.pass_context
def init(ctx, conf):
    ctx.obj['app'].init()
    with open(conf) as f:
        ctf_conf = yaml.safe_load(f)['ctf']
    timezone  = pytz.timezone(ctf_conf['timezone'])
    start_at  = timezone.localize(ctf_conf['start_at'])
    end_at    = timezone.localize(ctf_conf['end_at'])
    team_size = int(ctf_conf['team_size'])
    N = 0
    V = 100
    assert(type(eval(ctf_conf['score_exp'])) == int)
    assert(ctf_conf['admin_pass'] != '')

    ctx.obj['app'].initCTF(ctf_conf['name'], timezone, start_at, end_at, team_size, ctf_conf['score_exp'], ctf_conf['admin_pass'])
    print("[+]Done")


@cli.command()
@click.argument("directory")
@click.option("--only", type=str, default="")
@click.pass_context
def set_challenges(ctx, directory, only):
    if not ctx.obj['app'].getConfig('ctf_name'):
        print("[!]CTF configuration is uninitialized")
        exit()

    with open(os.path.join(directory, "challenges.yaml")) as f:
        all_challenges = yaml.safe_load(f)['challenges']

    if only:
        only = only.split(",")

    challenges = []
    for c in all_challenges:
        if not c['completed']:
            continue
        if only and c['name'] not in only:
            continue

        challenges.append(c)

    ctx.obj['app'].upsertChallenges(challenges)
    print("[+]Added challenges")
    for c in challenges:
        print("[+] {}".format(c['name']))

@cli.command()
@click.option('--all', is_flag=True)
@click.pass_context
def list_challenges(ctx, all):
    if not ctx.obj['app'].getConfig('ctf_name'):
        print("[!]CTF configuration is uninitialized")
        exit()

    challenges = ctx.obj['app'].allChallenges(all)
    for c in challenges:
        s = "`{}`\tby {}\t{}".format(c.name, c.author, "hidden" if c.hidden else "opened")
        print(s)

@cli.command()
@click.argument("challenges", type=str)
@click.pass_context
def open_challenges(ctx, challenges):
    if not ctx.obj['app'].getConfig('ctf_name'):
        print("[!]CTF configuration is uninitialized")
        exit()

    challenges = challenges.split(",")
    for cname in challenges:
        c = ctx.obj['app'].getChallenge(cname)
        c.hidden = False
        ctx.obj['app'].session.add(c)
    ctx.obj['app'].session.commit()
    print("[+]Done")
if __name__ == '__main__':
    cli()
