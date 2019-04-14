import unittest
from kosenctfkit.app import App
from kosenctfkit.config import Config
from datetime import datetime
import pytz


class Test(unittest.TestCase):
    def setUp(self):
        class TestConfig(Config):
            def __init__(self):
                super().__init__()
                self.SECRET_KEY = 'testsecret'
                self.DATABASE_URL = 'sqlite://'
                self.DEBUG = True

        self.app = App(TestConfig())
        tz = pytz.timezone('Asia/Tokyo')
        self.app.init()
        self.app.initCTF(
            ctf_name='TestCTF',
            timezone=tz,
            start_at=tz.localize(datetime.strptime('2019-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')),
            end_at=tz.localize(datetime.strptime('2020-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')),
            team_size=None,
            score_exp='V',
            admin_pass='admin'
        )

    def base_test(self):
        self.app.insertUser({
            'name': 'testUser',
            'password': 'password',
        })
        user = self.app.getUser('testUser')
        self.assertTrue(user.check_password('password'))
        self.assertFalse(user.check_password('bad password'))

        self.app.insertTeam({
            'name': 'testTeam'
        })
        team = self.app.getTeam('testTeam')
        self.app.joinTeam(user, team.token)

        self.assertTrue(self.app.getUser('testUser').team.id == team.id)
        self.assertTrue(self.app.getTeam('testTeam').members.first().id == user.id)

