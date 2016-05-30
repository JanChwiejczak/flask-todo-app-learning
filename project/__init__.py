from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('project._config')
db = SQLAlchemy(app)

from project import views