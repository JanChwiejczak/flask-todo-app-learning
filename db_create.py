# db_create.py

from project import db
from project.models import Task, User
from datetime import date

# Create db
db.create_all()

# admin user
db.session.add(User("admin", "maslo@admina.com", "admin", "admin"))

# Some example data
list_of_tasks = [('Finish this tutorial', date(2016,5,17), 10, 1),
                 ('Finish RP course', date(2016,6,30), 8, 1)]

# Insert Data
for t in list_of_tasks:
    db.session.add(Task(*t))
db.session.commit()
