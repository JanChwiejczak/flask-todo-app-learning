import datetime

from project.forms import AddTaskForm

from functools import wraps
from flask import Flask, flash, redirect, request, render_template, session, url_for, g
from sqlalchemy.exc import IntegrityError
# from flask.ext.sqlalchemy import SQLAlchemy

# config

# app = Flask(__name__)
# app.config.from_object('_config')
# db = SQLAlchemy(app)
from project import db, app
from project.models import Task, User

# helper functions


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Please login first.')
            return redirect(url_for('login'))
    return wrap


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error in the {} field - {}".format(getattr(form, field).label.text, error), 'error')


def open_tasks():
    return db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())


def closed_tasks():
    return db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())

########################
#### route handlers ####
########################

###



@app.route('/tasks/')
@login_required
def tasks():
    return render_template(
        'tasks.html',
        form=AddTaskForm(request.form),
        open_tasks=open_tasks(),
        closed_tasks=closed_tasks()
    )


@app.route('/add', methods=['GET', 'POST'])
@login_required
def new_task():
    error = None
    form = AddTaskForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_task = Task(
                form.name.data,
                form.due_date.data,
                form.priority.data,
                datetime.datetime.utcnow(),
                '1',
                session['user_id']
            )
            db.session.add(new_task)
            db.session.commit()
            flash('New entry was successfully posted. Thanks.')
            return redirect(url_for('tasks'))
    return render_template(
        'tasks.html',
        form=form,
        error=error,
        open_tasks=open_tasks(),
        closed_tasks=closed_tasks()
    )


@app.route('/complete/<int:task_id>')
@login_required
def complete(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id or session['user_role'] == 'admin':
        task.update({"status": "0"})
        db.session.commit()
        flash('The task is complete. Nice.')
    else:
        flash('You can only update tasks that belong to you')
    return redirect(url_for('tasks'))


@app.route('/delete/<int:task_id>')
@login_required
def delete_entry(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id or session['user_role'] == 'admin':
        task.delete()
        db.session.commit()
        flash('The task was deleted. Why not add a new one?')
    else:
        flash('You can only delete tasks that belong to you')
    return redirect(url_for('tasks'))

