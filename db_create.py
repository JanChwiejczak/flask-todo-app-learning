# db_create.py

from views import db
from models import Task
from datetime import date

# Create db
db.create_all()


# Some example data
list_of_tasks = [('Finish this tutorial', date(2016,5,17), 10, 1),
                 ('Finish RP course', date(2016,6,30), 8, 1)]

# Insert Data
for t in list_of_tasks:
    db.session.add(Task(*t))
db.session.commit()
