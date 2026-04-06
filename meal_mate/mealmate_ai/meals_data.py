import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "meals.db")

meals = [
    # Low calorie meals for weight loss
    ("Ugali and Sukuma", "lunch", 420, 350, "ugali,sukuma,vegetables", 12.5, 75.0, 8.0, "Cook ugali until firm. Steam sukuma with onions and tomatoes. Serve together."),
    ("Githeri", "lunch", 350, 300, "maize,beans,vegetables", 15.0, 60.0, 5.0, "Boil maize and beans together. Add vegetables and spices. Simmer until tender."),
    ("Matoke Stew", "dinner", 370, 400, "matoke,vegetables,onions", 8.0, 70.0, 6.0, "Peel and boil matoke. Cook vegetables with onions. Mash matoke and mix with stew."),
    ("Rice and Beans", "lunch", 400, 380, "rice,beans,vegetables", 18.0, 65.0, 7.0, "Cook rice separately. Boil beans with vegetables. Mix together and season."),
    ("Mandazi and Chai", "breakfast", 300, 200, "mandazi,tea", 8.0, 45.0, 12.0, "Fry mandazi dough. Brew tea with milk and sugar. Serve together."),
    ("Egg Sandwich", "breakfast", 320, 250, "bread,eggs,lettuce", 16.0, 35.0, 14.0, "Boil eggs. Toast bread. Assemble with lettuce and mayonnaise."),
    ("Vegetable Soup", "lunch", 250, 250, "carrots,spinach,tomatoes,onions", 6.0, 40.0, 4.0, "Chop vegetables. Boil in water with spices. Simmer until soft."),
    ("Greek Salad", "lunch", 280, 350, "lettuce,tomatoes,cucumbers,olives", 5.0, 25.0, 18.0, "Chop vegetables. Mix with olives and feta. Dress with olive oil."),

    # Medium calorie meals
    ("Chapati and Ndengu", "dinner", 480, 500, "chapati,ndengu,vegetables", 22.0, 55.0, 16.0, "Cook ndengu with spices. Make chapati dough and fry. Serve together."),
    ("Pilau", "lunch", 650, 800, "rice,spices,meat,vegetables", 28.0, 70.0, 25.0, "Fry meat and onions. Add rice and spices. Cook until rice is tender."),
    ("Chicken Stir Fry", "dinner", 550, 600, "chicken,rice,vegetables,soy sauce", 35.0, 50.0, 20.0, "Stir fry chicken. Add vegetables. Mix with cooked rice and soy sauce."),
    ("Fish and Chips", "dinner", 700, 750, "fish,potatoes,oil", 30.0, 60.0, 35.0, "Fry fish fillets. Deep fry potato chips. Serve with tartar sauce."),

    # High calorie meals for weight gain
    ("Beef Stew with Ugali", "dinner", 850, 1000, "beef,ugali,carrots,potatoes", 45.0, 80.0, 40.0, "Slow cook beef with vegetables. Serve with ugali."),
    ("Chicken Biryani", "dinner", 900, 900, "chicken,rice,spices,yogurt", 50.0, 85.0, 35.0, "Marinate chicken. Layer with rice and spices. Cook in oven."),
    ("Avocado Toast with Eggs", "breakfast", 650, 500, "bread,avocado,eggs,cheese", 25.0, 45.0, 40.0, "Mash avocado on toast. Top with poached eggs and cheese."),
    ("Pasta Carbonara", "dinner", 780, 800, "pasta,cream,bacon,cheese,eggs", 32.0, 65.0, 45.0, "Cook pasta. Mix with cream, bacon, eggs, and cheese."),
    ("Banana Smoothie Bowl", "breakfast", 600, 450, "bananas,yogurt,honey,nuts,granola", 18.0, 75.0, 22.0, "Blend bananas with yogurt. Top with nuts and granola."),
    ("Cheeseburger", "lunch", 750, 650, "beef patty,cheese,bun,lettuce,tomato", 35.0, 50.0, 45.0, "Grill beef patty. Assemble with cheese, veggies on bun."),
    ("Fried Rice with Meat", "dinner", 820, 850, "rice,meat,eggs,vegetables,oil", 38.0, 70.0, 40.0, "Fry meat and vegetables. Add rice and scrambled eggs."),
    ("Peanut Butter Sandwich", "breakfast", 580, 380, "bread,peanut butter,banana,honey", 20.0, 55.0, 30.0, "Spread peanut butter on bread. Add banana slices and honey."),

    # Budget-friendly meals (under 500 KES)
    ("Simple Ugali", "lunch", 380, 150, "ugali", 10.0, 75.0, 2.0, "Boil water. Add maize flour gradually while stirring until thick."),
    ("Bean Stew", "lunch", 320, 200, "beans,tomatoes,onions", 18.0, 50.0, 6.0, "Boil beans. Cook with tomatoes and onions. Season well."),
    ("Chapati Plain", "breakfast", 280, 120, "flour,oil", 8.0, 50.0, 8.0, "Make dough with flour and water. Roll and fry in oil."),
    ("Tea and Bread", "breakfast", 250, 140, "bread,tea,margarine", 6.0, 40.0, 10.0, "Toast bread with margarine. Brew tea with milk."),
    ("Corn and Beans", "lunch", 350, 180, "corn,beans", 16.0, 60.0, 5.0, "Boil corn and beans together. Season with salt."),
    ("Vegetable Stew", "dinner", 300, 220, "potatoes,carrots,cabbage", 8.0, 55.0, 4.0, "Boil vegetables together. Season with spices.")
]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Clear existing data and add new meals
cursor.execute("DELETE FROM meals")
cursor.executemany(
    "INSERT INTO meals (name, category, calories, price, ingredients, protein, carbs, fats, recipe) VALUES (?,?,?,?,?,?,?,?,?)",
    meals
)

conn.commit()
conn.close()

print("Meals database updated successfully!")