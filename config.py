from datetime import datetime
import pytz


class DefaultConfig:
    JSON_AS_ASCII = False

    # must be changed
    SECRET_KEY = "weak_key"
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = (
        "postgresql://kosenctfkit:kosenctfkit@kosenctfkit_db/kosenctfkit"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WEBHOOK_URL = (
        "https://hooks.slack.com/services/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"
    )
    INVITE_URL = "https://join.slack.com/t/xxxxxxxx/shared_invite/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    # google account for sending e-mail
    EMAIL = "kosenctf@example.com"
    EMAIL_PASSWORD = "emailaccountspassword"

    # CTF configurations
    CTF_NAME = "KosenCTF"
    FLAGFORMAT = "KosenCTF{[A-Za-z0-9_- !?#]+}"
    START_AT = pytz.timezone("Asia/Tokyo").localize(datetime(2019, 1, 1, 0, 0, 0))
    END_AT = pytz.timezone("Asia/Tokyo").localize(datetime(2020, 1, 1, 0, 0, 0))
    SCORE_EXPR = "max(200, (V*V) / (V + (V/10) * (0 if N == 1 else N)))"

    # administrator account
    ADMIN_NAME = "admin"
    ADMIN_PASSWORD = "password"

    # ssh configuration (key: hostname, value: ssh configuration name)
    SSH = {"localhost": "example"}

    # keep default
    STATIC_DIR = "static"
    ICON_DIR = "icons"

    # AWS: uncomment these if you want to use S3 instead of local directories
    # AWS_ACCESS_KEY = "AK******************"
    # AWS_ACCESS_SECRET = "****************************************"
    # S3_REGION = "ap-northeast-1"
    # S3_BUCKET = "kosenctf"


config = DefaultConfig()
