class DefaultConfig:
    SECRET_KEY = "weak_key"
    DEBUG = True
    JSON_AS_ASCII = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
