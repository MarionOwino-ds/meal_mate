# meal_chatbot.py

import random

# Sample meals by category
meal_suggestions = {
    "breakfast": ["Oatmeal with fruit", "Egg sandwich", "Smoothie bowl", "Pancakes", "Greek yogurt with granola"],
    "lunch": ["Chicken salad", "Rice and beans", "Tuna wrap", "Veggie stir-fry", "Pasta with tomato sauce"],
    "dinner": ["Grilled chicken and veggies", "Ramen with egg", "Fried rice", "Tacos", "Lentil soup"]
}

def suggest_meal(available_items):
    # Match user ingredients to meal suggestions
    matches = []
    for meal_list in meal_suggestions.values():
        for meal in meal_list:
            if any(item.lower() in meal.lower() for item in available_items):
                matches.append(meal)
    return matches if matches else ["Hmmm... maybe go with instant noodles? 🍜"]

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
    print("👩‍🍳 MealBot: Hey there, hungry student! Let’s figure out what you can eat.")
    while True:
        user_input = input("\nYou: ").strip().lower()

        if "bye" in user_input:
            print("👩‍🍳 MealBot: Take care! Eat something good! 🥗")
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
                print("👩‍🍳 MealBot: Please enter a number of days!")

        elif "option" in user_input or "ingredient" in user_input:
            items = input("List what you have (comma-separated): ").split(",")
            suggestions = suggest_meal([i.strip() for i in items])
            print("\n👩‍🍳 MealBot: Based on that, you could try:")
            for meal in suggestions:
                print(f" - {meal}")

        else:
            print("👩‍🍳 MealBot: You can ask for 'meal plan', or tell me your 'ingredients/options'!")

if __name__ == "__main__":
    main()