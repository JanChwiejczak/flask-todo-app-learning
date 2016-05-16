# db_create.py

import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:

    # Get connection cursor used to execute SQL commands
    c = connection.cursor()

    # Create Table
    c.execute("""CREATE TABLE tasks(
                 task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 due_date TEXT NOT NULL,
                 priority INTEGER NOT NULL,
                 status INTEGER NOT NULL
                 )""")

    # Some example data
    tasks = [('Finish this tutorial', '17/05/2016', 10, 1),
             ('Finish RP course', '31/05/2016', 8, 1)]

    c.executemany('INSERT INTO tasks (name, due_date, priority, status) VALUES (?,?,?,?)', tasks)
    
