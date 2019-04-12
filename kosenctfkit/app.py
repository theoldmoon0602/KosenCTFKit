from kosenctfkit.models import Base, Config, User, Challenge
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

class App():
    def __init__(self, config):
        self.config = config
        self.engine = create_engine(config.DATABASE_URL)
        self.session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))

    def init(self):
        Base.metadata.create_all(bind=self.engine)

    def reset(self):
        import contextlib
        with contextlib.closing(self.engine.connect()) as con:
            trans = con.begin()
            for table in reversed(Base.metadata.sorted_tables):
                con.execute(table.delete())
            trans.commit()
        Base.metadata.drop_all(bind=self.engine)

    def getConfig(self, key, default=None):
        return self.session.query(Config).filter(Config.key == key).first() or default

    def init_ctf(self, ctf_name, timezone, start_at, end_at, team_size, score_exp, admin_pass):

        self.session.add(Config(key="ctf_name", value=ctf_name))
        self.session.add(Config(key="timezone", value=timezone.zone))
        self.session.add(Config(key="start_at", value=start_at.timestamp()))
        self.session.add(Config(key="end_at", value=end_at.timestamp()))
        self.session.add(Config(key="team_size", value=team_size))
        self.session.add(Config(key="score_exp", value=score_exp))
        self.session.add(User(name="admin", password=admin_pass, admin=True, hidden=True))

        self.session.commit()

    def insert_challenges(self, challenges):
        for c in challenges:
            chal = self.session.query(Challenge).filter(Challenge.name == c['name']).first()
            if chal is None:
                chal = Challenge()

            chal.name        = c['name']
            chal.description = c['description']
            chal.author      = c['author']
            chal.testers     = ','.join(c['testers'])
            chal.flag        = c['flag']
            chal.score       = c['score']
            chal.category    = c['category']
            chal.visible     = False

            self.session.add(chal)
        self.session.commit()
