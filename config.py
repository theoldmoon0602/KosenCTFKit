import secrets
from kosenctfkit.config import Config


class ProductionConfig(Config):
    SECRET_KEY = secrets.token_hex(32)
    DEBUG = False


class DebugConfig(Config):
    SECRET_KEY = '0'*64
    DEBUG = True

