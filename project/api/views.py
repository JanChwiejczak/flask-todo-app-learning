from functools import wraps
from flask import flash, redirect, jsonify, session, url_for, Blueprint, make_response

from project import db
from project.models import Task

################# CONFIG #####################

api_blueprint = Blueprint('api', __name__)

################# HELPER FUNCTIONS ###########


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Please login first.')
            return redirect(url_for('users.login'))
    return wrap


def open_tasks():
    return db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())


def closed_tasks():
    return db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())

################# ROUTES ###########

@api_blueprint.route('/api/v1/tasks/')
def api_tasks():
    results = db.session.query(Task).limit(10).offset(0).all()
    json_results = []
    for result in results:
        data = {
            'task_id': result.task_id,
            'task name': result.name,
            'due date': str(result.due_date),
            'priority': result.priority,
            'posted date': str(result.posted_date),
            'status': result.status,
            'user_id': result.user_id
        }
        json_results.append(data)
    return jsonify(items=json_results)

@api_blueprint.route('/api/v1/tasks/<int:task_id>')
def complete(task_id):
    new_id = task_id
    result = db.session.query(Task).filter_by(task_id=new_id).first()
    if result:
        json_result = {
            'task_id': result.task_id,
            'task name': result.name,
            'due date': str(result.due_date),
            'priority': result.priority,
            'posted date': str(result.posted_date),
            'status': result.status,
            'user_id': result.user_id
        }
        code = 200
    else:
        json_result = {'error': 'No task with task_id={}'.format(new_id)}
        code = 404
    return make_response(jsonify(json_result), code)
