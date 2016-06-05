import datetime

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('project._config')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.tasks.views import tasks_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)

@app.errorhandler(404)
def not_found(error):
    if not app.debug:
        now = datetime.datetime.now()
        with open('error.log', 'a') as log:
            current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
            log.write("\n{} - 404 error : {}".format(current_timestamp, request.url))
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    if not app.debug:
        now = datetime.datetime.now()
        with open('error.log', 'a') as log:
            current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
            log.write("\n{} - 500 error : {}".format(current_timestamp, request.url))
    return render_template('500.html'), 500