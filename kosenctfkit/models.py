from datetime import datetime
from sqlalchemy import Column, Boolean, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import bcrypt

Base = declarative_base()

class Notification(Base):
    __tablename__ = 'notifications'

    id      = Column(Integer, primary_key=True)
    title   = Column(Text)
    content = Column(Text)
    date    = Column(DateTime, default=datetime.utcnow)

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    challenges = relationship('Challenge', backref='category')


class Challenge(Base):
    __tablename__ = 'challenges'

    id           = Column(Integer, primary_key=True)
    name         = Column(String(80))
    description  = Column(Text)
    flag         = Column(Text)
    max_attempts = Column(Integer, default=0)
    score        = Column(Integer)
    category_id  = Column(Integer, ForeignKey('categories.id'))
    state        = Column(String(80), nullable=False, default='visible')
    files        = relationship('Attachment', backref=backref('challenge', cascade='all, delete'))
    submissions  = relationship('Submission', backref='challenge')

    def __repr__(self):
        return '<Challenge {}>'.format(self.name)


class Attachment(Base):
    __tablename__ = 'attachments'

    id           = Column(Integer, primary_key=True)
    location     = Column(Text)
    challenge_id = Column(Integer, ForeignKey('challenges.id', ondelete='CASCADE'))

    def __repr__(self):
        return "<Attachment location={}>".format(location=self.location)


class User(Base):
    __tablename__ = 'users'

    id            = Column(Integer, primary_key=True)
    oauth_id      = Column(Integer, unique=True)
    name          = Column(String(128))
    email         = Column(String(128), unique=True)
    password_hash = Column(String(128))
    submissions   = relationship("Submission", backref="user")

    admin    = Column(Boolean, default=False)
    hidden   = Column(Boolean, default=False)
    banned   = Column(Boolean, default=False)
    verified = Column(Boolean, default=False)

    team_id    = Column(Integer, ForeignKey('teams.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=datetime.utcnow)

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


class Team(Base):
    __tablename__ = 'teams'

    id          = Column(Integer, primary_key=True)
    name        = Column(String(128), unique=True)
    email       = Column(String(128), unique=True)
    token       = Column(String(128), unique=True)
    members     = relationship("User", backref=backref("team", cascade='all, delete'))
    submissions = relationship("Submission", backref="team")

    hidden   = Column(Boolean, default=False)
    banned   = Column(Boolean, default=False)
    verified = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Team {}>'.format(self.name)


class Submission(Base):
    __tablename__ = 'submissions'

    id           = Column(Integer, primary_key=True)
    text         = Column(Text)
    challenge_id = Column(Integer, ForeignKey('challenges.id', ondelete='CASCADE'))
    user_id      = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    team_id      = Column(Integer, ForeignKey('teams.id', ondelete='CASCADE'))
    ip           = Column(String(46))
    created_at   = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Submission {}, {}, {}, {}>'.format(self.user, self.challenge, self.text)


class Config(Base):
    __tablename__ = 'config'

    id    = Column(Integer, primary_key=True)
    key   = Column(Text)
    value = Column(Text)
