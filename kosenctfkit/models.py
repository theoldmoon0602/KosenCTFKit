from gino import Gino
from datetime import datetime
import bcrypt

db = Gino()

class Notification(db.Model):
    __tablename__ = 'notifications'

    id      = db.Column(db.Integer, primary_key=True)
    title   = db.Column(db.Text)
    content = db.Column(db.Text)
    date    = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Challenge(db.Model):
    __tablename__ = 'challenges'

    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(80))
    description  = db.Column(db.Text)
    flag         = db.Column(db.Text)
    max_attempts = db.Column(db.Integer, default=0)
    score        = db.Column(db.Integer)
    category     = db.Column(db.String(80))
    state        = db.Column(db.String(80), nullable=False, default='visible')
    files        = db.relationship('Attachment', backref='challenge')
    submissions  = db.relationship('Submission', backref='challenge')

    def __repr__(self):
        return '<Challenge {}>'.format(self.name)


class Attachment(db.Model):
    __tablename__ = 'attachments'

    id           = db.Column(db.Integer, primary_key=True)
    location     = db.Column(db.Text)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'))

    def __repr__(self):
        return "<Attachment location={}>".format(location=self.location)


class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    oauth_id      = db.Column(db.Integer, unique=True)
    name          = db.Column(db.String(128))
    email         = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    submissions   = db.relationship("Submission", backref="team")

    hidden   = db.Column(db.Boolean, default=False)
    banned   = db.Column(db.Boolean, default=False)
    verified = db.Column(db.Boolean, default=False)

    team_id    = db.Column(db.Integer, db.ForeignKey('teams.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<User {}@{}>'.format(self.name, self.team)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plaintext):
        self.password_hash = bcrypt.hashpw(plaintext.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(self.password_hash.encode('utf-8'), password.encode('utf-8'))


class Team(db.Model):
    __tablename__ = 'teams'

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(128), unique=True)
    email       = db.Column(db.String(128), unique=True)
    token       = db.Column(db.String(128), unique=True)
    members     = db.relationship("User", backref="team")
    submissions = db.relationship("Submission", backref="team")

    hidden   = db.Column(db.Boolean, default=False)
    banned   = db.Column(db.Boolean, default=False)
    verified = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Team {}>'.format(self.name)


class Submission(db.Model):
    __tablename__ = 'submissions'

    id           = db.Column(db.Integer, primary_key=True)
    text         = db.Column(db.Text)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id', ondelete='CASCADE'))
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    team_id      = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='CASCADE'))
    ip           = db.Column(db.String(46))
    created_at   = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Submission {}, {}, {}, {}>'.format(self.user, self.challenge, self.text)


class Configs(db.Model):
    __tablename__ = 'config'

    id    = db.Column(db.Integer, primary_key=True)
    key   = db.Column(db.Text)
    value = db.Column(db.Text)
