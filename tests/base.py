import unittest

from greybook import create_app
from greybook.core.extensions import db
from greybook.models import Admin


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.app_context()
        self.context.push()
        self.client = self.app.test_client()
        self.cli_runner = self.app.test_cli_runner()

        db.create_all()
        user = Admin(
            name='Grey Li',
            username='admin',
            password='greybook',
            about='I am test blog',
            blog_title='Testlog',
            blog_sub_title='a test blog'
        )
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def login(self, username='admin', password='greybook'):
        return self.client.post(
            '/auth/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.client.get('/auth/logout', follow_redirects=True)
