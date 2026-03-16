import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "meals.db")

meals = [
    # Low calorie meals for weight loss
    ("Ugali and Sukuma", "lunch", 420, 80, "ugali,sukuma,vegetables"),
    ("Githeri", "lunch", 350, 70, "maize,beans,vegetables"),
    ("Matoke Stew", "dinner", 370, 100, "matoke,vegetables,onions"),
    ("Rice and Beans", "lunch", 400, 90, "rice,beans,vegetables"),
    ("Mandazi and Chai", "breakfast", 300, 50, "mandazi,tea"),
    ("Egg Sandwich", "breakfast", 320, 60, "bread,eggs,lettuce"),
    ("Vegetable Soup", "lunch", 250, 60, "carrots,spinach,tomatoes,onions"),
    ("Greek Salad", "lunch", 280, 85, "lettuce,tomatoes,cucumbers,olives"),

    # Medium calorie meals
    ("Chapati and Ndengu", "dinner", 480, 120, "chapati,ndengu,vegetables"),
    ("Pilau", "lunch", 650, 200, "rice,spices,meat,vegetables"),
    ("Chicken Stir Fry", "dinner", 550, 150, "chicken,rice,vegetables,soy sauce"),
    ("Fish and Chips", "dinner", 700, 180, "fish,potatoes,oil"),

    # High calorie meals for weight gain
    ("Beef Stew with Ugali", "dinner", 850, 250, "beef,ugali,carrots,potatoes"),
    ("Chicken Biryani", "dinner", 900, 220, "chicken,rice,spices,yogurt"),
    ("Avocado Toast with Eggs", "breakfast", 650, 120, "bread,avocado,eggs,cheese"),
    ("Pasta Carbonara", "dinner", 780, 190, "pasta,cream,bacon,cheese,eggs"),
    ("Banana Smoothie Bowl", "breakfast", 600, 110, "bananas,yogurt,honey,nuts,granola"),
    ("Cheeseburger", "lunch", 750, 160, "beef patty,cheese,bun,lettuce,tomato"),
    ("Fried Rice with Meat", "dinner", 820, 200, "rice,meat,eggs,vegetables,oil"),
    ("Peanut Butter Sandwich", "breakfast", 580, 90, "bread,peanut butter,banana,honey"),

    # Budget-friendly meals (under 100)
    ("Simple Ugali", "lunch", 380, 40, "ugali"),
    ("Bean Stew", "lunch", 320, 50, "beans,tomatoes,onions"),
    ("Chapati Plain", "breakfast", 280, 30, "flour,oil"),
    ("Tea and Bread", "breakfast", 250, 35, "bread,tea,margarine"),
    ("Corn and Beans", "lunch", 350, 45, "corn,beans"),
    ("Vegetable Stew", "dinner", 300, 55, "potatoes,carrots,cabbage")
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