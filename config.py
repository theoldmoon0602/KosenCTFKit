import secrets
import os
from kosenctfkit.config import Config


class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        self.SECRET_KEY = secrets.token_hex(32)
        self.DEBUG = False


class DebugConfig(Config):
    def __init__(self):
        super().__init__()
        self.SECRET_KEY = '0'*64
        self.DEBUG = True

        DBURL = os.getenv('DATABASE', None)
        if DBURL:
            self.DATABASE_URL = 'postgresql://'+DBURL
        else:
            self.DATABASE_URL = 'postgresql://kosenctfkit:kosenctfkit@localhost:5432/kosenctfkit'

