import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "meals.db")

meals = [
    # Low calorie meals for weight loss
    ("Ugali and Sukuma", "lunch", 420, 350, "ugali,sukuma,vegetables"),
    ("Githeri", "lunch", 350, 300, "maize,beans,vegetables"),
    ("Matoke Stew", "dinner", 370, 400, "matoke,vegetables,onions"),
    ("Rice and Beans", "lunch", 400, 380, "rice,beans,vegetables"),
    ("Mandazi and Chai", "breakfast", 300, 200, "mandazi,tea"),
    ("Egg Sandwich", "breakfast", 320, 250, "bread,eggs,lettuce"),
    ("Vegetable Soup", "lunch", 250, 250, "carrots,spinach,tomatoes,onions"),
    ("Greek Salad", "lunch", 280, 350, "lettuce,tomatoes,cucumbers,olives"),

    # Medium calorie meals
    ("Chapati and Ndengu", "dinner", 480, 500, "chapati,ndengu,vegetables"),
    ("Pilau", "lunch", 650, 800, "rice,spices,meat,vegetables"),
    ("Chicken Stir Fry", "dinner", 550, 600, "chicken,rice,vegetables,soy sauce"),
    ("Fish and Chips", "dinner", 700, 750, "fish,potatoes,oil"),

    # High calorie meals for weight gain
    ("Beef Stew with Ugali", "dinner", 850, 1000, "beef,ugali,carrots,potatoes"),
    ("Chicken Biryani", "dinner", 900, 900, "chicken,rice,spices,yogurt"),
    ("Avocado Toast with Eggs", "breakfast", 650, 500, "bread,avocado,eggs,cheese"),
    ("Pasta Carbonara", "dinner", 780, 800, "pasta,cream,bacon,cheese,eggs"),
    ("Banana Smoothie Bowl", "breakfast", 600, 450, "bananas,yogurt,honey,nuts,granola"),
    ("Cheeseburger", "lunch", 750, 650, "beef patty,cheese,bun,lettuce,tomato"),
    ("Fried Rice with Meat", "dinner", 820, 850, "rice,meat,eggs,vegetables,oil"),
    ("Peanut Butter Sandwich", "breakfast", 580, 380, "bread,peanut butter,banana,honey"),

    # Budget-friendly meals (under 500 KES)
    ("Simple Ugali", "lunch", 380, 150, "ugali"),
    ("Bean Stew", "lunch", 320, 200, "beans,tomatoes,onions"),
    ("Chapati Plain", "breakfast", 280, 120, "flour,oil"),
    ("Tea and Bread", "breakfast", 250, 140, "bread,tea,margarine"),
    ("Corn and Beans", "lunch", 350, 180, "corn,beans"),
    ("Vegetable Stew", "dinner", 300, 220, "potatoes,carrots,cabbage")
]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Clear existing data and add new meals
cursor.execute("DELETE FROM meals")
cursor.executemany(
    "INSERT INTO meals (name, category, calories, price, ingredients) VALUES (?,?,?,?,?)",
    meals
)

conn.commit()
conn.close()

print("Meals database updated successfully!")