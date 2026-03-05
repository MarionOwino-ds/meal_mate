import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "meals.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS meals(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    calories INTEGER,
    price INTEGER,
    ingredients TEXT
)
""")

conn.commit()
conn.close()

print("Database and table 'meals' created successfully!")