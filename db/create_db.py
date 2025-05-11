import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        date TEXT NOT NULL DEFAULT (CURRENT_DATE)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS habits (
               id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
               habit TEXT NOT NULL,
               description TEXT, 
               date DATE NOT NULL,
               interval INTEGER NOT NULL
    )
''')

conn.commit()
conn.close()