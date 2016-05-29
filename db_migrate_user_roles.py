from views import db
from _config import DATABASE_PATH

import sqlite3
from datetime import datetime

with sqlite3.connect(DATABASE_PATH) as connection:

    c = connection.cursor()
    c.execute("""ALTER TABLE users RENAME TO old_users""")

    # Recreates the DB with new schema
    db.create_all()

    c.execute("""SELECT id, name, email, password
              FROM old_users ORDER BY id ASC""")
    data = [(row[0], row[1], row[2], row[3], 'user') for row in c.fetchall()]

    c.executemany("""INSERT INTO users (id, name, email, password, role)
                  VALUES (?,?,?,?,?)""", data)
    c.execute("DROP TABLE old_users")