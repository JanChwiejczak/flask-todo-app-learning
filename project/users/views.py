from functools import wraps
from flask import flash, redirect, request, render_template, session, url_for, Blueprint

from .forms import RegisterForm, LoginForm
from project import db, bcrypt
from project.models import User


################# CONFIG #####################

users_blueprint = Blueprint('users', __name__)

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

################# ROUTES ###########


@users_blueprint.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('user_role', None)
    session.pop('user_name', None)
    flash('Goodbye!')
    return redirect(url_for('users.login'))

@users_blueprint.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['name']).first()
            if user and bcrypt.check_password_hash(user.password, request.form['password']):
                session['logged_in'] = True
                session['user_id'] = user.id
                session['user_role'] = user.role
                session['user_name'] = user.name
                flash('Welcome')
                return redirect(url_for('tasks.tasks'))
            elif not user:
                form.name.errors.append('Username not recognized')
            else:
                form.password.errors.append('Incorrect password')
    return render_template('login.html', form=form)


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                form.name.data,
                form.email.data,
                bcrypt.generate_password_hash(form.password.data)
            )
            user_exist = db.session.query(User).filter_by(name=new_user.name).first()
            email_exist = db.session.query(User).filter_by(email=new_user.email).first()
            if user_exist:
                form.name.errors.append('Username already taken')
            if email_exist:
                form.email.errors.append('Email already in use')
            if not (user_exist or email_exist):
                db.session.add(new_user)
                db.session.commit()
                flash('Thank you for registering. Please Login')
                return redirect(url_for('users.login'))
    return render_template('register.html', form=form)