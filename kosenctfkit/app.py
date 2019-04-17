from kosenctfkit.models import Base, Config, User, Team, Challenge, Submission
from sqlalchemy import create_engine
from sqlalchemy.sql import func
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

    @property
    def ctf_name(self):
        return self.getConfig('ctf_name', '')

    @property
    def team_size(self):
        return float(self.getConfig('team_size', 'inf'))

    @property
    def score_exp(self):
      return self.getConfig('score_exp')

    def getConfig(self, key, default=None):
        v = self.session.query(Config).filter(Config.key == key).first()
        if v and v.value is not None:
            return v.value
        return default

    def initCTF(self, ctf_name, timezone, start_at, end_at, team_size, score_exp, admin_pass):

        self.session.add(Config(key="ctf_name", value=ctf_name))
        self.session.add(Config(key="timezone", value=timezone.zone))
        self.session.add(Config(key="start_at", value=start_at.timestamp()))
        self.session.add(Config(key="end_at", value=end_at.timestamp()))
        self.session.add(Config(key="team_size", value=team_size))
        self.session.add(Config(key="score_exp", value=score_exp))
        self.session.add(User(name="admin", password=admin_pass, admin=True, hidden=True))

        self.session.commit()

    def upsertChallenges(self, challenges):
        for c in challenges:
            chal = self.session.query(Challenge).filter(Challenge.name == c['name']).first()
            if chal is None:
                chal = Challenge()

            if isinstance(c, dict):
                vs = c
            else:
                vs = c.__dict__

            chal.name        = vs['name']
            chal.category    = vs['category']
            chal.flag        = vs['flag']
            chal.description = vs.get('description')
            chal.author      = vs.get('author')
            chal.testers     = ','.join(vs.get('testers', ''))
            chal.score       = vs['score']
            chal.hidden      = vs.get('hidden', True)

            self.session.add(chal)
        self.session.commit()

    def makeUser(self, user):
        u = User()
        u.name = user['name']
        u.password = user['password']
        u.email = user.get('email')
        u.admin = user.get('admin', False)
        u.hidden = user.get('hidden', False)
        u.team_id = user.get('team_id', None)

        return u

    def insertTeam(self, team):
        from secrets import token_hex

        t = Team()
        t.name = team['name']
        t.email = team.get('email')
        t.hidden = team.get('hidden', False)
        t.token = token_hex(16)

        self.session.add(t)
        self.session.commit()

        return t

    def renewTeamToken(self, team):
        from secrets import token_hex

        team.token = token_hex(16)
        self.session.add(team)
        self.session.commit()

        return team

    def joinTeam(self, user, team_token):
        t = self.session.query(Team).filter(Team.token == team_token).first()
        if t is None:
            raise ValueError("Invalid token")

        team_size = self.team_size
        if team_size <= t.members.count() + 1:
            raise ValueError("Team size overflow")

        user.team_id = t.id
        t.valid = True
        self.session.add(user)
        self.session.add(t)
        self.session.commit()

        return t

    def insertSubmission(self, submission, user, challenge):
        s = Submission(user_id=user.id, challenge_id=challenge.id)
        if user.team:
            s.team_id = user.team.id
        s.text = submission
        s.solved = Submission == challenge.flag
        solvedby_user_or_team = self.session.query(Submission).filter(
          Submission.challenge_id == challenge.id,
          Submission.valid == True,
          Submission.user_id == user.id,
          Submission.team_id == user.team.id
        ).first()
        s.valid = s.solved and solvedby_user_or_team is None

        self.session.add(s)
        self.session.commit()

    def getUser(self, name):
        return self.session.query(User).filter(User.name == name).first()

    def getChallenge(self, name):
        return self.session.query(Challenge).filter(Challenge.name == name).first()

    def getTeam(self, name):
        return self.session.query(Team).filter(Team.name == name).first()

    def allUsers(self):
      return self.session.query(User).filter(User.hidden==False).all()

    def allTeams(self):
      return self.session.query(Team).filter(Team.hidden==False, Team.valid == True).all()

    def allChallenges(self, all=False):
        if all:
            return self.session.query(Challenge).all()
        else:
            return self.session.query(Challenge).filter(Challenge.hidden==False).all()


    def _calcScore(self, challenges):
      solved_cids = [c.id for c in challenges]
      cid_score_counts = self.session.query(Challenge.id, Challenge.score, func.count(Submission.id)).group_by(
        Challenge.id
      ).filter(
        Submission.valid == True,
      ).all()

      exp = self.score_exp
      score = 0
      for x in cid_score_counts:
        cid, V, N = x
        if cid in solved_cids:
          score += eval(exp)
        return score

    def userSolves(self, user, valid_only=False):
        solves = self.session.query(Challenge).join(
          Challenge.hidden == False,
          Submission.valid == True if valid_only else Submission.solved == True,
          Submission.user_id == user.id,
          Submission.challenge_id == Challenge.id,
        ).all()
        return solves

    def userScore(self, user):
      solves = self.userSolves(user, valid_only=True)
      return self._calcScore(solves)

    def teamSolves(self, team, valid_only=False):
      solves = self.session.query(Challenge).join(
        Challenge.hidden == False,
        Submission.valid == True if valid_only else Submission.solved == True,
        Submission.team_id == team.id,
        Submission.challenge_id == Challenge.id,
      ).all()
      return solves

    def teamScore(self, team):
      solves = self.teamSolves(team, valid_only=True)
      return self._calcScore(solves)

    def allUserScores(self):
      users = self.allUsers()
      submissions = self.session.query(Submission).filter(Submission.valid == True).all()
      challenges = self.allChallenges()

      values = {u.id:[u.name, 0, 0] for u in users}

      chal_solves = {}
      for s in submissions:
        chal_solves[s.challenge_id] = chal_solves.get(s.challenge_id, 0) + 1

      exp = self.score_exp
      chal_scores = {}
      for c in challenges:
        N = chal_solves[c.id]
        V = c.score
        chal_scores[c.id] = eval(exp)

      for s in submissions:
        values[s.user_id][1] += chal_scores[s.challenge_id]
        values[s.user_id][2] = max(values[s.user_id][2], s.created_at)

      return values

    def allTeamScores(self):
      teams = self.allTeams()
      submissions = self.session.query(Submission).filter(Submission.valid == True).all()
      challenges = self.allChallenges()

      values = {t.id:[t.name, 0, 0] for t in teams}

      chal_solves = {}
      for s in submissions:
        chal_solves[s.challenge_id] = chal_solves.get(s.challenge_id, 0) + 1

      exp = self.score_exp
      chal_scores = {}
      for c in challenges:
        N = chal_solves[c.id]
        V = c.score
        chal_scores[c.id] = eval(exp)

      for s in submissions:
        values[s.team_id][1] += chal_scores[s.challenge_id]
        values[s.team_id][2] = max(values[s.team_id][2], s.created_at)

      return values
