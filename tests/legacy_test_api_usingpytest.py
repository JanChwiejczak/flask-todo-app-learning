import os
import pytest

from project import app as _app
from project import db as _db
from project import bcrypt
from project.models import User, Task


basedir = os.path.abspath(os.path.dirname(__file__))
TEST_DB = 'test.db'
TEST_DB_URI = 'sqlite:///' + os.path.join(basedir, TEST_DB)

@pytest.fixture(scope='session')
def app():
    """session wide Flask application"""
    settings_override = {
        'DEBUG': False,
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': TEST_DB_URI
    }
    _app.config.from_object(settings_override)
    return _app.test_client()

@pytest.fixture(scope="session")
def db(app, request):
    """session wide test database"""

    def teardown():
        _db.session.remove()
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalier(teardown)
    return _db


def test__is_app_running(app, db):
    response = app.get('/', follow_redirects=True)
    assert response.status_code == 200