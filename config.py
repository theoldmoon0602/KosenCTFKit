class DefaultConfig:
    SECRET_KEY = "weak_key"
    DEBUG = True
    JSON_AS_ASCII = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WEBHOOK_URL = (
        "https://hooks.slack.com/services/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"
    )
    STATIC_DIR = "static"
    ICON_DIR = "icons"
