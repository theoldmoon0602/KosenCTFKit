from datetime import datetime
import pytz


class DefaultConfig:
    SECRET_KEY = "weak_key"
    DEBUG = True
    JSON_AS_ASCII = False
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://kosenctfkit:kosenctfkit@localhost:5432/kosenctfkit"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WEBHOOK_URL = (
        "https://hooks.slack.com/services/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"
    )
    STATIC_DIR = "static"
    ICON_DIR = "icons"

    CTF_NAME = "KosenCTF"
    START_AT = pytz.timezone("Asia/Tokyo").localize(datetime(2019, 1, 1, 0, 0, 0))
    END_AT = pytz.timezone("Asia/Tokyo").localize(datetime(2020, 1, 1, 0, 0, 0))
    SCORE_EXPR = "max(200, (V*V) / (V + (V/10) * (0 if N == 1 else N)))"
    ADMIN_NAME = "admin"
    ADMIN_PASSWORD = "password"
    SSH = {"localhost": "example"}


config = DefaultConfig()
