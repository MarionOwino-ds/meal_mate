import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "meals.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop table if exists to ensure fresh schema
cursor.execute("DROP TABLE IF EXISTS meals")

cursor.execute("""
CREATE TABLE meals(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    calories INTEGER,
    price INTEGER,
    ingredients TEXT,
    protein REAL,
    carbs REAL,
    fats REAL,
    recipe TEXT
)
""")

conn.commit()
conn.close()

print("Database and table 'meals' created successfully!")