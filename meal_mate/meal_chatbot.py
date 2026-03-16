# mealmate.py

import random


meal_suggestions = {
    "breakfast": [
        "Chai and mandazi",
        "Uji (millet porridge)",
        "Bread and eggs",
        "Sweet potatoes and tea",
        "Chapati and beans"
        'indomie'
    ],
    "lunch": [
        "Ugali and sukuma wiki",
        "Rice and beans",
        "Githeri",
        "Pilau and kachumbari",
        "Chapati and ndengu"
        'smocha '
        'samosa'
    ],
    "dinner": [
        "Ugali and eggs",
        "Mukimo and beef stew",
        "Matoke with vegetables",
        "Rice and lentils",
        "Ndengu stew with chapati"
    ]
}

def suggest_meal(available_items):
    matches = []
    for meal_list in meal_suggestions.values():
        for meal in meal_list:
            if any(item.lower() in meal.lower() for item in available_items):
                matches.append(meal)
    return matches if matches else ["Maybe grab some chips and soda? 🍟🥤"]

def create_meal_plan(days=3):
    plan = {}
    for day in range(1, days + 1):
        plan[f"Day {day}"] = {
            "Breakfast": random.choice(meal_suggestions["breakfast"]),
            "Lunch": random.choice(meal_suggestions["lunch"]),
            "Dinner": random.choice(meal_suggestions["dinner"])
        }
    return plan

def main():
    print("🍴 MealMate:Mambo Comrade ")
    while True:
        user_input = input("\nYou: ").strip().lower()

        if "bye" in user_input:
            print("🍴 MealMate: Kwaheri! Stay full and healthy! 😊")
            break

        elif "plan" in user_input:
            days = input("How many days should I plan for? (1-7): ")
            try:
                days = int(days)
                plan = create_meal_plan(days)
                for day, meals in plan.items():
                    print(f"\n📅 {day}:")
                    for meal_time, meal in meals.items():
                        print(f"  {meal_time}: {meal}")
            except ValueError:
                print("🍴 MealMate: Tafadhali, enter a number!")

        elif "option" in user_input or "ingredient" in user_input:
            items = input("List what you have (comma-separated): ").split(",")
            suggestions = suggest_meal([i.strip() for i in items])
            print("\n🍴 MealMate: Based on that, you could try:")
            for meal in suggestions:
                print(f" - {meal}")

        else:
            print("🍴 MealMate: You can ask for a 'meal plan', or tell me your 'ingredients/options'!")

if __name__ == "__main__":
    main()