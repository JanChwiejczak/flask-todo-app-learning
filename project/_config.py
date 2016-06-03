import os

# Grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
WTF_CSRF_ENABLED = True
SECRET_KEY = b'P\x15\xc2\x9a\xa3f^~\x94-\x16\xf7\x1f\xd2t\xffv}Ij\xd3z\xd4\xe4'

# define the full path for database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database URI
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False

# for deployment
DEBUG = False
