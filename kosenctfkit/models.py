from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    icon = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    submissions = db.relationship("Submission", backref="user", lazy=True)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, pw):
        self.password_hash = bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, pw):
        return bcrypt.checkpw(pw.encode("utf-8"), self.password_hash)

    def getSolves(self, valid_only):
        solves = (
            Challenge.query.join(Challenge, Submission)
            .filter(
                Submission.challenge_id == Challenge.id,
                Submission.is_valid == True
                if valid_only
                else Submission.is_correct == True,
                Submission.user_id == self.id,
            )
            .all()
        )
        return solves

    def getScore(self, valid_only):
        solves = self.getSolves(valid_only)
        score = 0
        for c in solves:
            score += c.score
        return score


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    token = db.Column(db.String(256), unique=True, nullable=False)
    members = db.relationship("User", backref="team", lazy=True)
    valid = db.Column(db.Boolean, nullable=False, default=False)
    submissions = db.relationship("Submission", backref="team", lazy=True)

    def getSolves(self, valid_only):
        solves = (
            Challenge.query.join(Challenge, Submission)
            .filter(
                Submission.challenge_id == Challenge.id,
                Submission.is_valid == True
                if valid_only
                else Submission.is_correct == True,
                Submission.team_id == self.id,
            )
            .all()
        )
        return solves

    def getScore(self, valid_only):
        solves = self.getSolves(valid_only)
        score = 0
        for c in solves:
            score += c.score
        return score

    def renewToken(self):
        from secrets import token_hex

        self.token = token_hex(16)


class Challenge(db.Model):
    __tablename__ = "challenges"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, unique=True, nullable=False)
    flag = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)
    tester_array = db.Column(db.Text, nullable=False)
    base_score = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    is_open = db.Column(db.Boolean, nullable=False, default=False)
    attachements = db.relationship("Attachment", backref="challenge", lazy=True)

    @property
    def testers(self):
        return self.tester_array.split(",")

    @testers.setter
    def testers(self, tester_list):
        self.tester_array = ",".join(tester_list)


class Attachment(db.Model):
    __tablename__ = "attachements"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)


class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)
    flag = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    created_at = db.Column(
        db.Integer, nullable=False, default=lambda: datetime.utcnow().timestamp()
    )
    is_valid = db.Column(db.Boolean, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)


class Config(db.Model):
    __tablename__ = "config"

    name = db.Column(db.String, nullable=False, primary_key=True)
    start_at = db.Column(db.Integer, nullable=False)
    end_at = db.Column(db.Integer, nullable=False)
    is_open = db.Column(db.Boolean, nullable=False)
    register_open = db.Column(db.Boolean, nullable=False)
    score_expr = db.Column(db.Text, nullable=False)

    @property
    def isopen(self):
        return self.is_open and (
            self.start_at <= datetime.utcnow().timestamp() < self.end_at
        )

    @staticmethod
    def get():
        return Config.query.first()


class Log(db.Model):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.Integer, nullable=False, default=lambda: datetime.utcnow().timestamp()
    )


def init_db(app):
    db.init_app(app)
