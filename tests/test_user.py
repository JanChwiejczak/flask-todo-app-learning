import os
import unittest
from project import app, db
from project.models import User

basedir = os.path.abspath(os.path.dirname(__file__))
TEST_DB = 'test.db'


class AllTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['DEBUG'] = False
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

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def register(self, usr, pwd, email='', confirm=''):
        if not confirm:
            confirm = pwd
        if not email:
            email = usr+'@example.com'
        return self.app.post(
            '/register',
            data=dict(name=usr, email=email, password=pwd, confirm=confirm),
            follow_redirects=True
        )

    def create_user(self, name, email, password, role=None):
        new_user = User(name=name, email=email, password=bcrypt.generate_password_hash(password), role=role)
        db.session.add(new_user)
        db.session.commit()

    def test_user_can_register(self):
        new_user = User('michael', 'michael@mherman.org', 'michaelherman')
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).first()
        assert test.name == 'michael'

    def test_users_cannot_login_unless_registered(self):
        response = self.login('fakeuser', 'fakepassword')
        self.assertIn(b'Username not recognized', response.data)

    # Form validation tests
    # Should be changed to flask testing assert redirects from response stream checks

    def test_form_is_present_on_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login to access your task list', response.data)

    def test_user_can_login(self):
        self.register(usr='JanTesting', pwd='tpassword')
        response = self.login('JanTesting', 'tpassword')
        self.assertIn(b'Add a new task', response.data)

    def test_invalid_login_form_data(self):
        self.register(usr='JanTesting', pwd='tpassword')
        response = self.login('DROP TABLE User; alert("alert box!";', 'tpassword')
        self.assertIn(b'Username not recognized', response.data)

    def test_form_is_present_on_register_page(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access your task list', response.data)

    def test_user_registration(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register(usr='JanTesting', pwd='tpassword')
        self.assertIn(b'Thank you for registering. Please Login', response.data)

    def test_user_registration_error_username_taken(self):
        self.app.get('/register', follow_redirects=True)
        self.register(usr='JanTesting', pwd='tpassword', email='JanTest@gmail.com')
        self.app.get('/register', follow_redirects=True)
        response = self.register(usr='JanTesting', pwd='tpassword', email='another@gmail.com')
        self.assertIn(b'Username already taken', response.data)

    def test_user_registration_error_email_taken(self):
        self.app.get('/register', follow_redirects=True)
        self.register(usr='JanTesting', pwd='tpassword', email='JanTest@gmail.com')
        self.app.get('/register', follow_redirects=True)
        response = self.register(usr='DifferentJan', pwd='tpassword', email='JanTest@gmail.com')
        self.assertIn(b'Email already in use', response.data)

    def test_logged_in_users_can_logout(self):
        self.register('Testerthatwilllogout', 'anothertest101')
        self.login('Testerthatwilllogout', 'anothertest101')
        response = self.logout()
        self.assertIn(b'Goodbye!', response.data)
        # Should also assert redirect to login

    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b'Goodbye!', response.data)

    def test_string_representation_of_the_user_object(self):
        new_user = User('michael', 'michael@mherman.org', 'michaelherman')
        db.session.add(new_user)
        db.session.commit()
        assert new_user.name == 'michael'

    def test_default_user_role(self):
        new_user = User('Johnnny', 'michael@comsemase.org', 'michaelherman')
        db.session.add(new_user)
        db.session.commit()

        user = db.session.query(User).first()
        self.assertEquals(user.role, 'user')

    def test_User_default_representation(self):
        new_user = User(name='Mikosan', email='miko@gmail.com', password='password')
        self.assertEqual(new_user.__repr__(), '<User Mikosan>')
