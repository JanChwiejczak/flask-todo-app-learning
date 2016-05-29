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

    def login_go_to_tasks(self, name, email, password):
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    def login_go_to_tasks(self, name, password):
        email = name+"@example.com"
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        self.login(name, password)
        self.app.get('/tasks/', follow_redirects=True)

    # TESTS

    def test_logged_in_users_can_access_tasks(self):
        self.register('Testerthatwilllogout', 'anothertest101')
        self.login('Testerthatwilllogout', 'anothertest101')
        response = self.app.get('/tasks/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a new task:', response.data)

    def test_not_logged_in_users_cannot_access_tasks(self):
        response = self.app.get('/tasks/', follow_redirects=True)
        self.assertIn(b'Please login first.', response.data)

    def test_users_can_add_tasks(self):
        self.login_go_to_tasks('Testarossa', 's0mepa455')
        response = self.create_task('Go to bank', '05/25/2017', '5')
        self.assertIn(b'New entry was successfully posted. Thanks.', response.data)

    def test_users_cannot_add_tasks_when_error(self):
        self.login_go_to_tasks('Mikosan', 'password')
        response = self.create_task('Go to bank', '', '5')
        self.assertIn(b'This field is required.', response.data)

    def test_users_can_complete_tasks(self):
        self.login_go_to_tasks('Testarossa', 's0mepa455')
        self.create_task('Go to bank', '05/25/2017', '5')
        response = self.app.get('/complete/1', follow_redirects=True)
        self.assertIn(b'The task is complete. Nice.', response.data)

    def test_users_can_delete_tasks(self):
        self.login_go_to_tasks('Testarossa', 's0mepa455')
        self.create_task('Go to bank', '05/25/2017', '5')
        response = self.app.get('/delete/1', follow_redirects=True) # should check whether it actually was removed from dbase
        self.assertIn(b'The task was deleted. Why not add a new one?', response.data)

    def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
        self.login_go_to_tasks('Testarossa', 's0mepa455')
        self.create_task('Go to bank', '05/25/2017', '5')
        self.logout()
        self.login_go_to_tasks('Mikosan', 'password')
        response = self.app.get('/complete/1', follow_redirects=True)
        self.assertNotIn(b'The task is complete. Nice.', response.data)
        self.assertIn(b'You can only update tasks that belong to you', response.data)

    def test_users_cannot_delete_tasks_that_are_not_created_by_them(self):
        self.login_go_to_tasks('Adriano', 'Marcepano')
        self.create_task('new task for adriano', '08/12/2016', '7')
        self.logout()
        self.login_go_to_tasks('Mikosan', 'password')
        response = self.app.get('/delete/1', follow_redirects=True)
        self.assertNotIn(b'The task was deleted. Why not add a new one?', response.data)
        self.assertIn(b'You can only delete tasks that belong to you', response.data)