import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "meals.db")

meals = [
    ("Ugali and Sukuma", "lunch", 420, 80, "ugali,sukuma"),
    ("Githeri", "lunch", 350, 70, "maize,beans"),
    ("Chapati and Ndengu", "dinner", 480, 120, "chapati,ndengu"),
    ("Rice and Beans", "lunch", 400, 90, "rice,beans"),
    ("Mandazi and Chai", "breakfast", 300, 50, "mandazi,tea"),
    ("Egg Sandwich", "breakfast", 320, 60, "bread,eggs"),
    ("Matoke Stew", "dinner", 370, 100, "matoke,vegetables"),
    ("Pilau", "lunch", 650, 200, "rice,spices,meat")
]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.executemany(
    "INSERT INTO meals (name, category, calories, price, ingredients) VALUES (?,?,?,?,?)",
    meals
)

conn.commit()
conn.close()

print("Meals added successfully!")