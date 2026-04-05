# 🍴 DormChef AI — A Kenyan Meal Suggestion Chatbot for Students

**DormChef AI** is an intelligent meal recommendation chatbot that helps university students plan meals based on their dietary goals, budget, and available ingredients.
It focuses on affordable and common **Kenyan dishes** that students love!

---

## ✨ Features
- 🤖 AI-powered chat interface with Streamlit
- 🥘 Intelligent meal suggestions based on ingredients, goals, and preferences
- 💰 Budget-friendly meal recommendations
- ⚖️ Weight loss/gain meal planning
- 🥗 Dietary restriction support (vegetarian, vegan, gluten-free, low-carb)
- 🧠 Smart intent parsing and meal database
- 🌐 Web-based interface (no terminal required)
- 📊 Nutritional information and cooking tips
- 🎯 Personalized recommendations

---

## 🇰🇪 Sample Dishes
- **Breakfast:** Mandazi and Chai, Avocado Toast with Eggs, Banana Smoothie Bowl
- **Lunch:** Ugali and Sukuma, Githeri, Pilau, Rice and Beans
- **Dinner:** Chicken Biryani, Beef Stew with Ugali, Matoke Stew, Vegetable Stew

---

## 🚀 How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/MarionOwino-ds/meal_mate.git
   cd meal_mate/mealmate_ai
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   python database.py  # Creates the meals table
   python meals_data.py  # Populates with sample data
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py --server.headless true
   ```

5. Open your browser and start chatting with DormChef AI!

---

## 💬 How to Use DormChef AI

### **Getting Started**
- **Welcome Message:** The app greets you and explains what it can do
- **Chat Interface:** Type your meal requests in the input box at the bottom
- **Conversation History:** All your interactions are saved during the session

### **What You Can Ask**

#### **🎯 Dietary Goals**
- `"I want to lose weight"` - Get low-calorie meal suggestions
- `"I need to gain weight"` - Get high-calorie, nutrient-dense options
- `"I'm on a budget"` - Get affordable meal ideas under $80

#### **🥘 Ingredient-Based Queries**
- `"Meals with chicken and rice"` - Find recipes using specific ingredients
- `"What can I make with beans?"` - Discover dishes from available ingredients
- `"Rice and vegetable options"` - Combine multiple ingredients

#### **🍽️ Meal Types**
- `"Breakfast ideas"` - Morning meal suggestions
- `"Lunch options"` - Midday meal recommendations
- `"Dinner suggestions"` - Evening meal ideas

#### **🥗 Dietary Restrictions**
- `"Vegetarian meals"` - Plant-based options only
- `"Vegan recipes"` - No animal products whatsoever
- `"Gluten-free options"` - Wheat-free meal ideas
- `"Low-carb meals"` - Reduced carbohydrate options

#### **💰 Budget Queries**
- `"Cheap meals"` - Meals under $80
- `"Budget-friendly dinner"` - Affordable evening options
- `"Inexpensive breakfast"` - Low-cost morning meals

### **Example Conversations**

```
You: I want to lose weight
DormChef: Great choice for staying healthy! Here are some lighter meal options:

1. **Vegetable Soup** (lunch)
   • Calories: 250 | Price: $60
   • Ingredients: carrots, spinach, tomatoes, onions
   • Quick tip: Ready in 20 minutes!

2. **Tea and Bread** (breakfast)
   • Calories: 250 | Price: $35
   • Ingredients: bread, tea, margarine
   • Health note: Low in calories, high in fiber

You: Cheap meals with chicken
DormChef: Smart thinking! Here are some wallet-friendly meal ideas:

1. **Chicken Stir Fry** (dinner)
   • Calories: 550 | Price: $150
   • Ingredients: chicken, rice, vegetables, soy sauce
   • Budget tip: Use seasonal vegetables to save more!

You: Vegetarian dinner ideas
DormChef: Perfect! Here are some delicious plant-based dinner options:

1. **Vegetable Stew** (dinner)
   • Calories: 300 | Price: $55
   • Ingredients: potatoes, carrots, cabbage
   • Nutrition: High in vitamins A and C!
```

### **Understanding the Responses**

Each meal suggestion includes:
- **Meal Name & Type:** What it is and when to eat it
- **Nutrition Info:** Calories and estimated cost
- **Ingredients:** What's needed to make it
- **Smart Tips:** Cooking advice, health notes, or budget tips

### **Tips for Better Results**
- **Be Specific:** "Low-calorie chicken dinner" works better than just "food"
- **Combine Preferences:** "Budget vegetarian lunch with beans"
- **Use Keywords:** Include words like "cheap", "healthy", "quick", "easy"
- **Try Variations:** If you don't like suggestions, ask for "something else"

---

## 🧪 Testing

Run the test scripts to verify functionality:
```bash
python test_db.py      # Check database contents
python test_chatbot.py # Test chatbot responses
```

---

## 🧠 How It Works

- **Intent Parsing:** Analyzes your message to understand goals, preferences, and restrictions
- **Smart Filtering:** Searches the meal database for matching criteria
- **Personalized Responses:** Provides contextual tips and nutritional information
- **Fallback Handling:** Offers alternatives when exact matches aren't found

---

## 🤝 Contributing

Feel free to suggest new features or report issues! This app is designed to help students eat better on a budget.

---

## 🧪 Testing

Run the test scripts to verify functionality:
```bash
python test_db.py      # Check database contents
python test_chatbot.py # Test chatbot responses
```

---

## 🧠 How It Works

- **Intent Parsing:** Analyzes user input to understand goals (weight loss/gain, budget), dietary restrictions, and ingredient preferences
- **Smart Filtering:** Queries SQLite database for meals matching criteria
- **Response Formatting:** Provides formatted meal suggestions with calories, prices, and ingredients
- **Fallback Handling:** Offers alternatives when no exact matches are found

---
