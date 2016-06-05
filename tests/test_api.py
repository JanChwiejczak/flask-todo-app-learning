import os
import unittest
from project import app, db, bcrypt
from project.models import User, Task


basedir = os.path.abspath(os.path.dirname(__file__))
TEST_DB = 'test.db'


class AllTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['DEBUG'] = True
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

    def create_task(self, name, due_date, priority):
        return self.app.post(
            '/add',
            data=dict(
                name=name,
                due_date=due_date,
                priority=priority
            ),
            follow_redirects=True
        )

    def login_go_to_tasks(self, name, password, role=None):
        email = name+"@example.com"
        new_user = User(name=name, email=email, password=bcrypt.generate_password_hash(password), role=role)
        db.session.add(new_user)
        db.session.commit()
        self.login(name, password)
        self.app.get('/tasks/', follow_redirects=True)

    # TESTS

    def test_collection_endpoint_returns_correct_data(self):
        self.login_go_to_tasks('NowyTester', 'Hiccupss')
        self.create_task('Visit RT23423', '05/25/2017', '5')
        self.create_task('Go to and test H082934', '05/25/2017', '5')
        self.logout()
        response = self.app.get('api/v1/tasks/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(response.data, b'Visit RT23423')
        self.assertIn(response.data, b'Go to and test H082934')