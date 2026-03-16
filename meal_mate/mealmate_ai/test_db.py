import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "meals.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT * FROM meals")
rows = cursor.fetchall()
conn.close()

if rows:
    print("Database has meals:")
    for row in rows:
        print(row)
else:
    print("Database is empty!")