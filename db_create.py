# db_create.py

from project import db, bcrypt
from project.models import Task, User
from datetime import date

# Create db
db.create_all()

# admin user
password = bcrypt.generate_password_hash('admin')
db.session.add(User("admin", "maslo@admina.com", password, "admin"))

# Some example data
list_of_tasks = [('Finish this tutorial', date(2016,5,17), 10, date(2016,5,10), 1, 1),
                 ('Finish RP course', date(2016,6,30), 8, date(2016,5,10), 1, 1)]

# Insert Data
for t in list_of_tasks:
    db.session.add(Task(*t))
db.session.commit()
