from datetime import datetime
from sqlalchemy import Column, Boolean, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from responder_login import UserMixin
import bcrypt

Base = declarative_base()

class Notification(Base):
    __tablename__ = 'notifications'

    id      = Column(Integer, primary_key=True)
    title   = Column(Text)
    content = Column(Text)
    date    = Column(DateTime, default=datetime.utcnow)


class Challenge(Base):
    __tablename__ = 'challenges'

    id          = Column(Integer, primary_key=True)
    name        = Column(String(80), unique=True, nullable=False)
    description = Column(Text, default='')
    author      = Column(String(80), default='')
    testers     = Column(Text, default='')
    flag        = Column(Text, nullable=False)
    score       = Column(Integer, nullable=False)
    category    = Column(String(80), default='')
    hidden      = Column(String(80), nullable=False, default=True)
    files       = relationship('Attachment', backref=backref('challenge', cascade='all, delete'))
    submissions = relationship('Submission', backref='challenge')

    def __repr__(self):
        return '<Challenge {}>'.format(self.name)


class Attachment(Base):
    __tablename__ = 'attachments'

    id           = Column(Integer, primary_key=True)
    location     = Column(Text)
    challenge_id = Column(Integer, ForeignKey('challenges.id', ondelete='CASCADE'))

    def __repr__(self):
        return "<Attachment location={}>".format(location=self.location)


class User(Base, UserMixin):
    __tablename__ = 'users'

    id            = Column(Integer, primary_key=True)
    name          = Column(String(128), unique=True, nullable=False)
    email         = Column(String(128), unique=True)
    password_hash = Column(String(128), nullable=False)
    submissions   = relationship("Submission", backref="user")

    admin    = Column(Boolean, default=False)
    hidden   = Column(Boolean, default=False)
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
    name        = Column(String(128), unique=True, nullable=False)
    email       = Column(String(128), unique=True)
    token       = Column(String(128), unique=True, nullable=False)
    members     = relationship("User", backref=backref("team", cascade='all, delete'))
    submissions = relationship("Submission", backref="team")

    hidden   = Column(Boolean, default=False)
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
    solved       = Column(Boolean, nullable=False)
    valid        = Column(Boolean, nullable=False)
    created_at   = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Submission {}, {}, {}, {}>'.format(self.user, self.challenge, self.text)


class Config(Base):
    __tablename__ = 'config'

    id    = Column(Integer, primary_key=True)
    key   = Column(Text, unique=True)
    value = Column(Text)
