from kosenctfkit.models import Base
from sqlalchemy import create_engine


def init_app(config):
    engine = create_engine(config.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
