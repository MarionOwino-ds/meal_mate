import sqlite3
import os
import random
import re
from contextlib import contextmanager
from typing import List, Dict, Optional, Tuple

DB_PATH = os.path.join(os.path.dirname(__file__), "meals.db")

# Global storage for last recommendations (simple session)
last_recommendations = []

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
        SELECT name, category, calories, price, ingredients, protein, carbs, fats, recipe
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
            'ingredients': row[4],
            'protein': row[5],
            'carbs': row[6],
            'fats': row[7],
            'recipe': row[8]
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

    # Enhanced intro messages with emojis and personality
    if intent['goal'] == 'lose_weight':
        intro_templates = [
            "💪 **Great choice for staying healthy!** Here are some lighter meal options that will keep you energized:",
            "🎯 **Perfect for your weight loss goals!** These meals are lower in calories but high in nutrition:",
            "🌱 **I love helping with healthy eating!** Check out these nutritious, lower-calorie options:"
        ]
    elif intent['goal'] == 'gain_weight':
        intro_templates = [
            "💪 **Awesome! Let's fuel up with some hearty meals** to help you build strength:",
            "🏋️ **Perfect for building muscle!** Here are some calorie-dense options packed with nutrients:",
            "⚡ **Great choice for gaining!** These meals will help you pack on the calories you need:"
        ]
    elif intent['goal'] == 'budget':
        intro_templates = [
            "💰 **Smart thinking!** Here are some wallet-friendly meal ideas that won't break the bank:",
            "🤑 **Budget-friendly and delicious!** Check out these affordable options:",
            "💸 **Perfect for saving money** without sacrificing taste or nutrition:"
        ]
    else:
        intro_templates = [
            "🍽️ **Sounds delicious!** Here are some amazing meal suggestions just for you:",
            "🤤 **I've got some great options for you** that I think you'll love:",
            "✨ **You might enjoy these meals** - they're popular choices among students:"
        ]

    intro = random.choice(intro_templates)

    # Enhanced meal formatting with tips and nutritional info
    meal_lines = []
    cooking_tips = {
        'breakfast': ['Quick to prepare - perfect for busy mornings!', 'High in protein to start your day right!', 'Great source of sustained energy!'],
        'lunch': ['Balanced nutrition for your midday meal!', 'Keeps you full until dinner!', 'Rich in vitamins and minerals!'],
        'dinner': ['Hearty and satisfying for evening meals!', 'Helps you recover and rest well!', 'Nutrient-dense for overnight recovery!']
    }

    health_tips = {
        'lose_weight': ['Low in calories, high in fiber!', 'Helps maintain healthy weight!', 'Nutrient-dense for fewer calories!'],
        'gain_weight': ['Calorie-dense for muscle building!', 'High in healthy fats and proteins!', 'Perfect for active lifestyles!'],
        'budget': ['Affordable without compromising nutrition!', 'Uses common, inexpensive ingredients!', 'Great value for money!']
    }

    for i, meal in enumerate(meals[:4], 1):  # Show top 4 meals
        ingredients_list = meal['ingredients'].replace(',', ', ')

        # Determine meal category for tips
        category = meal['category']
        goal = intent.get('goal', 'general')

        # Get contextual tips
        category_tip = random.choice(cooking_tips.get(category, ['Delicious and nutritious!']))
        health_tip = random.choice(health_tips.get(goal, ['Balanced and healthy!']))

        meal_lines.append(f"**{i}. 🍽️ {meal['name']}** *({meal['category'].title()})*")
        meal_lines.append(f"   • **Calories:** {meal['calories']} kcal | **Price:** KES {meal['price']}")
        meal_lines.append(f"   • **Nutrition:** Protein: {meal['protein']}g | Carbs: {meal['carbs']}g | Fats: {meal['fats']}g")
        meal_lines.append(f"   • **Ingredients:** {ingredients_list}")
        meal_lines.append(f"   • **Recipe:** {meal['recipe']}")
        meal_lines.append(f"   • **💡 Tip:** {category_tip}")
        meal_lines.append(f"   • **🌟 Health:** {health_tip}")
        meal_lines.append("")  # Empty line for spacing

    response = intro + "\n\n" + "\n".join(meal_lines)

    if len(meals) > 4:
        response += f"\n*...and {len(meals) - 4} more delicious options available! Ask me to show more!*"

    # Add encouragement based on goal
    if intent['goal'] == 'lose_weight':
        response += "\n\n💪 **Remember:** Consistency is key! Combine these meals with regular exercise for best results."
    elif intent['goal'] == 'gain_weight':
        response += "\n\n🏋️ **Pro tip:** Pair these meals with strength training for optimal muscle growth!"
    elif intent['goal'] == 'budget':
        response += "\n\n🤑 **Money-saving hack:** Buy ingredients in bulk and cook in batches for even more savings!"

    return response

def get_no_results_response(intent: Dict) -> str:
    # More helpful and engaging no-results responses
    if intent['goal'] == 'lose_weight':
        responses = [
            "🤔 Hmm, I don't have many low-calorie options matching your criteria. How about trying some of our lighter meals under 500 calories? They're nutritious and satisfying!",
            "💭 Let me check our lighter options... Actually, try being less specific about ingredients and I'll show you some healthy, low-calorie choices that are perfect for weight loss!",
            "🎯 No exact matches, but I can suggest some naturally lower-calorie meals. Would you like to see options under 500 calories? They're great for maintaining a healthy weight!"
        ]
    elif intent['goal'] == 'gain_weight':
        responses = [
            "💪 Looking for more calorie-dense options? Let me show you our heartier meals that are perfect for building strength and gaining healthy weight!",
            "🏋️ I might not have exactly what you're looking for, but check out these higher-calorie options packed with nutrients for muscle building:",
            "⚡ Let's focus on some more substantial meals. Here are our calorie-rich options that will help you fuel up and gain weight effectively!"
        ]
    elif intent['goal'] == 'budget':
        responses = [
            "💰 Let me find some more affordable options for you! Here are our cheapest meals that still provide great nutrition and flavor:",
            "🤑 Budget-friendly meals coming right up! Here are our most affordable options that won't break the bank:",
            "💸 I can show you meals under KES 500 that are both delicious and nutritious. Perfect for student budgets!"
        ]
    else:
        responses = [
            "🔍 I couldn't find exact matches for those ingredients, but don't worry! Try different words or be less specific, and I'll find some delicious alternatives!",
            "🤔 Hmm, let me think of something else. How about trying some of our most popular meals? They're loved by students everywhere!",
            "✨ No direct matches, but I can suggest some delicious alternatives that use similar ingredients. Would you like to see them?"
        ]

    response = random.choice(responses)

    try:
        # Get fallback meals based on intent
        if intent['goal'] == 'budget':
            fallback_meals = get_meals_by_criteria(max_price=500, limit=3)
        elif intent['goal'] == 'lose_weight':
            fallback_meals = get_meals_by_criteria(max_calories=500, limit=3)
        elif intent['goal'] == 'gain_weight':
            fallback_meals = get_meals_by_criteria(min_calories=600, limit=3)
        else:
            fallback_meals = get_meals_by_criteria(limit=3)

        if fallback_meals:
            response += "\n\n🍽️ **Here are some great alternatives:**\n"
            for i, meal in enumerate(fallback_meals, 1):
                response += f"• **{meal['name']}** - KES {meal['price']}, {meal['calories']} cal\n"
    except Exception:
        pass

    return response

def generate_shopping_list(meals: List[Dict]) -> str:
    """Generate a shopping list from selected meals"""
    all_ingredients = set()
    for meal in meals:
        ingredients = meal['ingredients'].split(',')
        all_ingredients.update([ing.strip() for ing in ingredients])

    if not all_ingredients:
        return "No ingredients found for shopping list."

    shopping_list = sorted(list(all_ingredients))
    list_text = "\n".join([f"• {item.title()}" for item in shopping_list])

    total_cost = sum(meal['price'] for meal in meals)
    total_calories = sum(meal['calories'] for meal in meals)

    response = f"🛒 **Shopping List for {len(meals)} Meal{'s' if len(meals) > 1 else ''}**\n\n"
    response += f"**Ingredients Needed:**\n{list_text}\n\n"
    response += f"**Estimated Total Cost:** KES {total_cost}\n"
    response += f"**Total Calories:** {total_calories} kcal\n\n"
    response += "💡 **Tip:** Check your pantry first - you might already have some of these!"

    return response

def get_chatbot_response(user_input: str) -> str:
    global last_recommendations
    if not user_input or not user_input.strip():
        return "👋 Hey there! What kind of meal are you in the mood for? Tell me about your preferences!"

    # Handle common greetings and questions - check for exact matches first
    input_lower = user_input.lower().strip()

    # Exact greeting matches
    greetings = ['hello', 'hi', 'hey', 'mambo', 'habari', 'howdy']
    greeting_phrases = ['good morning', 'good afternoon', 'good evening', 'hi there', 'hello there']

    is_greeting = (
        input_lower in greetings or
        any(phrase in input_lower for phrase in greeting_phrases) or
        (len(input_lower.split()) <= 2 and any(greeting in input_lower for greeting in greetings))
    )

    if is_greeting:
        return "👋 **Mambo!** (Hello in Swahili! 🇰🇪) I'm DormChef AI, your Kenyan meal recommendation expert! What are you craving today? Tell me about your ingredients, budget, or dietary goals!"

    help_keywords = ['help', 'what can you do', 'how do you work', 'commands', 'examples', 'what are you']
    if any(keyword in input_lower for keyword in help_keywords):
        if 'shopping' in input_lower or 'shop' in input_lower or 'buy' in input_lower:
            return """🛒 **Shopping List Generator**

I can create a shopping list from meal recommendations! Just ask for meals first, then say "create shopping list" or "what do I need to buy?"

**Example:**
1. "Show me breakfast ideas"
2. "Create a shopping list for these meals"

This will give you all ingredients needed and estimated costs!"""
            return """🤖 **I'm DormChef AI, your smart meal planning assistant!**

**I can help you with:**
• **Dietary goals:** Weight loss/gain, healthy eating
• **Budget meals:** Affordable options under KES 500
• **Ingredients:** Recipes using what you have
• **Restrictions:** Vegetarian, vegan, gluten-free
• **Meal types:** Breakfast, lunch, dinner ideas
• **Meal Plans:** Generate weekly meal plans
• **Shopping Lists:** Generate shopping lists from recommendations

**Try asking:**
• "I want to lose weight"
• "Cheap meals with chicken"
• "Vegetarian dinner ideas"
• "What can I make with beans?"
• "Create a meal plan for me"
• "Generate shopping list"

What would you like to explore today? 🍽️"""

    # Handle meal plan requests
    plan_keywords = ['meal plan', 'weekly plan', 'plan meals', 'diet plan']
    if any(keyword in input_lower for keyword in plan_keywords):
        intent = parse_user_intent(user_input)
        return generate_meal_plan(intent)

    # Handle shopping list requests
    shopping_keywords = ['shopping list', 'create shopping', 'generate shopping', 'what do i need', 'ingredients list', 'shop', 'buy']
    if any(keyword in input_lower for keyword in shopping_keywords):
        if last_recommendations:
            return generate_shopping_list(last_recommendations)
        else:
            return "🤔 I don't have any recent meal recommendations to create a shopping list from. Try asking for meal suggestions first!"

    try:
        intent = parse_user_intent(user_input)

        query_params = {}

        if intent['goal'] == 'lose_weight':
            query_params['max_calories'] = 500
        elif intent['goal'] == 'gain_weight':
            query_params['min_calories'] = 600
        elif intent['goal'] == 'budget':
            query_params['max_price'] = 500

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

        # Store recommendations globally
        last_recommendations = meals

        response = format_meal_response(meals, intent)

        return response

    except Exception as e:
        return "😅 Oops! Something went wrong on my end. Let me try a different approach - what kind of meal sounds good to you? You can tell me about ingredients, budget, or dietary preferences!"

def get_meals_by_ingredient(ingredient):
    meals = get_meals_by_criteria(ingredients=[ingredient])
    return [m['name'] for m in meals]

def weight_loss_meals():
    meals = get_meals_by_criteria(max_calories=450)
    return [m['name'] for m in meals]

def budget_meals():
    meals = get_meals_by_criteria(max_price=120)
    return [m['name'] for m in meals]

def generate_meal_plan(intent: Dict, days: int = 7) -> str:
    """Generate a meal plan based on user preferences"""
    plan = []

    for day in range(1, days + 1):
        day_meals = {}

        # Get meals for each category
        for category in ['breakfast', 'lunch', 'dinner']:
            meals = get_meals_by_criteria(
                category=category,
                min_calories=600 if intent.get('goal') == 'gain_weight' else None,
                max_calories=500 if intent.get('goal') == 'lose_weight' else None,
                max_price=500 if intent.get('goal') == 'budget' else None,
                dietary_restrictions=intent.get('dietary_restrictions', []),
                limit=3
            )
            if meals:
                day_meals[category] = random.choice(meals)

        plan.append((day, day_meals))

    # Format the plan
    response = f"📅 **Your {days}-Day Meal Plan**\n\n"
    total_cost = 0
    total_calories = 0

    for day, meals in plan:
        response += f"**Day {day}:**\n"
        for category, meal in meals.items():
            response += f"• **{category.title()}:** {meal['name']} ({meal['calories']} cal, KES {meal['price']})\n"
            total_cost += meal['price']
            total_calories += meal['calories']
        response += "\n"

    response += f"**📊 Plan Summary:**\n"
    response += f"• Total Estimated Cost: KES {total_cost}\n"
    response += f"• Average Daily Calories: {total_calories // days}\n"
    response += f"• Total Meals: {len(plan) * 3}\n\n"

    if intent.get('goal') == 'lose_weight':
        response += "💪 **Weight Loss Focus:** This plan emphasizes lower-calorie, nutrient-dense meals!\n"
    elif intent.get('goal') == 'gain_weight':
        response += "🏋️ **Muscle Building Focus:** Higher calorie meals to support your gains!\n"
    elif intent.get('goal') == 'budget':
        response += "💰 **Budget-Friendly:** All meals under KES 500 for cost savings!\n"

    response += "\n🛒 Say 'create shopping list' to get ingredients for this plan!"

    return response