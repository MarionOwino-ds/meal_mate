import sqlite3
import os
import random
import re
from contextlib import contextmanager
from typing import List, Dict, Optional, Tuple

DB_PATH = os.path.join(os.path.dirname(__file__), "meals.db")

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()

def get_meals_by_criteria(
    min_calories: Optional[int] = None,
    max_calories: Optional[int] = None,
    max_price: Optional[int] = None,
    category: Optional[str] = None,
    ingredients: Optional[List[str]] = None,
    dietary_restrictions: Optional[List[str]] = None,
    limit: int = 10
) -> List[Dict]:
    with get_db_connection() as conn:
        cursor = conn.cursor()

        query = """
        SELECT name, category, calories, price, ingredients
        FROM meals WHERE 1=1
        """
        params = []

        if min_calories is not None:
            query += " AND calories >= ?"
            params.append(min_calories)

        if max_calories is not None:
            query += " AND calories <= ?"
            params.append(max_calories)

        if max_price is not None:
            query += " AND price <= ?"
            params.append(max_price)

        if category:
            query += " AND category = ?"
            params.append(category)

        if ingredients and len(ingredients) > 0:
            for ingredient in ingredients:
                query += " AND ingredients LIKE ?"
                params.append(f"%{ingredient}%")

        if dietary_restrictions:
            for restriction in dietary_restrictions:
                if restriction == 'vegetarian':
                    meat_ingredients = ['chicken', 'beef', 'pork', 'fish', 'meat', 'lamb', 'turkey', 'bacon']
                    for meat in meat_ingredients:
                        query += " AND ingredients NOT LIKE ?"
                        params.append(f"%{meat}%")
                elif restriction == 'vegan':
                    animal_ingredients = ['chicken', 'beef', 'pork', 'fish', 'meat', 'lamb', 'turkey', 'bacon', 'cheese', 'milk', 'yogurt', 'eggs', 'butter']
                    for animal in animal_ingredients:
                        query += " AND ingredients NOT LIKE ?"
                        params.append(f"%{animal}%")

        query += " ORDER BY calories ASC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [{
            'name': row[0],
            'category': row[1],
            'calories': row[2],
            'price': row[3],
            'ingredients': row[4]
        } for row in rows]

def parse_user_intent(user_input: str) -> Dict:
    input_lower = user_input.lower().strip()

    intent = {
        'goal': None,
        'category': None,
        'ingredients': [],
        'dietary_restrictions': [],
        'max_price': None,
        'meal_type': None
    }

    goal_keywords = {
        'lose_weight': ['lose weight', 'weight loss', 'slimming', 'diet', 'light', 'low calorie', 'healthy eating'],
        'gain_weight': ['gain weight', 'weight gain', 'bulking', 'muscle', 'high calorie', 'heavy', 'calorie dense'],
        'budget': ['cheap', 'budget', 'affordable', 'inexpensive', 'low cost', 'economical']
    }

    for goal, keywords in goal_keywords.items():
        if any(keyword in input_lower for keyword in keywords):
            intent['goal'] = goal
            for keyword in keywords:
                input_lower = input_lower.replace(keyword, '')
            break

    dietary_keywords = {
        'vegetarian': ['vegetarian', 'no meat', 'plant based', 'veggie'],
        'vegan': ['vegan', 'no animal', 'plant only', 'dairy free'],
        'gluten_free': ['gluten free', 'no gluten', 'celiac'],
        'low_carb': ['low carb', 'keto', 'ketogenic', 'no carbs']
    }

    for restriction, keywords in dietary_keywords.items():
        if any(keyword in input_lower for keyword in keywords):
            intent['dietary_restrictions'].append(restriction)
            for keyword in keywords:
                input_lower = input_lower.replace(keyword, '')
            break

    category_keywords = {
        'breakfast': ['breakfast', 'morning', 'brunch'],
        'lunch': ['lunch', 'midday', 'noon'],
        'dinner': ['dinner', 'evening', 'supper', 'dinner time']
    }

    for category, keywords in category_keywords.items():
        if any(keyword in input_lower for keyword in keywords):
            intent['category'] = category
            for keyword in keywords:
                input_lower = input_lower.replace(keyword, '')
            break

    food_words = {
        'chicken', 'beef', 'fish', 'rice', 'beans', 'pasta', 'bread', 'eggs', 'cheese',
        'vegetables', 'carrots', 'spinach', 'tomatoes', 'onions', 'potatoes', 'lettuce',
        'banana', 'apple', 'orange', 'milk', 'yogurt', 'butter', 'oil', 'flour', 'sugar',
        'meat', 'pork', 'lamb', 'turkey', 'duck', 'salmon', 'tuna', 'shrimp', 'crab',
        'corn', 'wheat', 'oats', 'nuts', 'peanuts', 'almonds', 'cashews', 'walnuts',
        'honey', 'salt', 'pepper', 'spices', 'herbs', 'garlic', 'ginger', 'chili',
        'pasta', 'noodles', 'soup', 'stew', 'curry', 'pizza', 'burger', 'sandwich',
        'salad', 'cereal', 'pancakes', 'waffles', 'toast', 'muffin', 'cake', 'pie',
        'ugali', 'matoke', 'githeri', 'pilau', 'chapati', 'mandazi', 'chai', 'ndengu',
        'sukuma', 'maize', 'avocado', 'mango', 'pineapple', 'strawberry', 'grape'
    }

    stop_words = {
        'i', 'want', 'like', 'some', 'a', 'an', 'the', 'for', 'with', 'and', 'or', 'but',
        'in', 'on', 'at', 'to', 'from', 'by', 'meal', 'food', 'eat', 'eating', 'hungry',
        'craving', 'ideas', 'options', 'something', 'anything', 'please', 'can', 'you',
        'me', 'my', 'give', 'show', 'find', 'looking', 'search', 'need', 'would', 'could',
        'should', 'about', 'that', 'this', 'these', 'those', 'what', 'how', 'when', 'where',
        'why', 'which', 'who', 'much', 'many', 'good', 'great', 'nice', 'delicious', 'tasty'
    }

    words = re.findall(r'\b\w+\b', input_lower)
    potential_ingredients = []

    for word in words:
        if word not in stop_words and len(word) > 2:
            if word in food_words:
                potential_ingredients.append(word)
            elif not word.endswith(('ing', 'ly', 'ed', 'er', 'est', 's')) and word not in {'meal', 'food', 'dish', 'plate'}:
                for food in food_words:
                    if word in food or food in word or word[:4] == food[:4]:
                        potential_ingredients.append(word)
                        break

    intent['ingredients'] = list(set(potential_ingredients))[:3]

    return intent

def format_meal_response(meals: List[Dict], intent: Dict) -> str:
    if not meals:
        return get_no_results_response(intent)

    if intent['goal'] == 'lose_weight':
        intro_templates = [
            "Great choice for staying healthy! Here are some lighter meal options:",
            "Perfect for your weight loss goals! These meals are lower in calories:",
            "I love helping with healthy eating! Check out these nutritious, lower-calorie options:"
        ]
    elif intent['goal'] == 'gain_weight':
        intro_templates = [
            "Awesome! Let's fuel up with some hearty meals:",
            "Perfect for building strength! Here are some calorie-dense options:",
            "Great choice for gaining! These meals will help you pack on the calories:"
        ]
    elif intent['goal'] == 'budget':
        intro_templates = [
            "Smart thinking! Here are some wallet-friendly meal ideas:",
            "Budget-friendly and delicious! Check these out:",
            "Perfect for saving money without sacrificing taste:"
        ]
    else:
        intro_templates = [
            "Sounds delicious! Here are some meal suggestions:",
            "I've got some great options for you:",
            "You might enjoy these meals:"
        ]

    intro = random.choice(intro_templates)

    meal_lines = []
    for i, meal in enumerate(meals[:5], 1):
        ingredients_list = meal['ingredients'].replace(',', ', ')
        meal_lines.append(f"{i}. **{meal['name']}** ({meal['category']})")
        meal_lines.append(f"   • Calories: {meal['calories']} | Price: ${meal['price']}")
        meal_lines.append(f"   • Ingredients: {ingredients_list}")

    response = intro + "\n\n" + "\n".join(meal_lines)

    if len(meals) > 5:
        response += f"\n\n...and {len(meals) - 5} more options available!"

    return response

def get_no_results_response(intent: Dict) -> str:
    if intent['goal'] == 'lose_weight':
        responses = [
            "Hmm, I don't have many low-calorie options right now. How about trying some of our lighter meals under 500 calories?",
            "Let me check our lighter options... Actually, try being less specific about ingredients and I'll show you some healthy choices!",
            "No exact matches, but I can suggest some naturally lower-calorie meals. Would you like to see options under 500 calories?"
        ]
    elif intent['goal'] == 'gain_weight':
        responses = [
            "Looking for more calorie-dense options? Let me show you our heartier meals!",
            "I might not have exactly what you're looking for, but check out these higher-calorie options:",
            "Let's focus on some more substantial meals. Here are our calorie-rich options:"
        ]
    elif intent['goal'] == 'budget':
        responses = [
            "Let me find some more affordable options for you:",
            "Budget-friendly meals coming right up! Here are our cheapest options:",
            "I can show you meals under $10. How does that sound?"
        ]
    else:
        responses = [
            "I couldn't find exact matches for those ingredients. Try different words or be less specific!",
            "Hmm, let me think of something else. How about trying some popular meals?",
            "No direct matches, but I can suggest some delicious alternatives!"
        ]

    response = random.choice(responses)

    try:
        fallback_meals = get_meals_by_criteria(limit=3)
        if fallback_meals:
            response += "\n\nHere are some popular options instead:\n"
            for meal in fallback_meals:
                response += f"• {meal['name']} (${meal['price']}, {meal['calories']} cal)\n"
    except Exception:
        pass

    return response

def get_chatbot_response(user_input: str) -> str:
    if not user_input or not user_input.strip():
        return "Hey there! What kind of meal are you in the mood for? Tell me about your preferences!"

    try:
        intent = parse_user_intent(user_input)

        query_params = {}

        if intent['goal'] == 'lose_weight':
            query_params['max_calories'] = 500
        elif intent['goal'] == 'gain_weight':
            query_params['min_calories'] = 600
        elif intent['goal'] == 'budget':
            query_params['max_price'] = 100

        if intent['category']:
            query_params['category'] = intent['category']

        if intent['ingredients']:
            query_params['ingredients'] = intent['ingredients']

        meals = get_meals_by_criteria(
            min_calories=query_params.get('min_calories'),
            max_calories=query_params.get('max_calories'),
            max_price=query_params.get('max_price'),
            category=query_params.get('category'),
            ingredients=query_params.get('ingredients'),
            dietary_restrictions=intent.get('dietary_restrictions', [])
        )

        response = format_meal_response(meals, intent)

        return response

    except Exception as e:
        return "Oops! Something went wrong on my end. Let me try a different approach - what kind of meal sounds good to you?"

def get_meals_by_ingredient(ingredient):
    meals = get_meals_by_criteria(ingredients=[ingredient])
    return [m['name'] for m in meals]

def weight_loss_meals():
    meals = get_meals_by_criteria(max_calories=450)
    return [m['name'] for m in meals]

def budget_meals():
    meals = get_meals_by_criteria(max_price=120)
    return [m['name'] for m in meals]

def random_response():
    responses = [
        "Hmm… let me think 🤔",
        "Okay I found something for you!",
        "Nice! Here are some ideas:",
        "You might enjoy these meals!"
    ]
    return random.choice(responses)