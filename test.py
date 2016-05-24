import os
import unittest
from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'


class AllTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Helper methods
    def login(self, name, password):
        return self.app.post('/', data=dict(name=name, password=password), follow_redirects=True)

    def register(self, name, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(name=name, email=email,password=password,confirm=confirm),
            follow_redirects=True
        )

    # Unit tests

    def test_user_can_register(self):
        new_user = User('michael', 'michael@mherman.org', 'michaelherman')
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            assert t.name == 'michael'

    def test_form_is_present_on_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login to access your task list', response.data)

    def test_users_cannot_login_unless_registered(self):
        response = self.login('fakeuser', 'fakepassword')
        self.assertIn(b'Invalid username or password', response.data)

    # Form validation tests
    # Should be changed to flask testing assert redirects from response stream checks

    def test_user_can_login(self):
        self.register('JanTesting', 'janny@gmail.com', 'tpassword', 'tpassword')
        response = self.login('JanTesting', 'tpassword')
        self.assertIn(b'Add a new task', response.data)

    def test_invalid_login_form_data(self):
        self.register('JanTesting', 'janny@gmail.com', 'tpassword', 'tpassword')
        response = self.login('DROP TABLE User; alert("alert box!";', 'tpassword')
        self.assertIn(b'Invalid username or password', response.data)

if __name__ == '__main__':
    unittest.main()