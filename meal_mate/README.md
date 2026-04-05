# 🍴 DormChef AI — A Kenyan Meal Suggestion Chatbot for Students

**DormChef AI** is an intelligent meal recommendation chatbot that helps university students plan meals based on their dietary goals, budget, and available ingredients.
It focuses on affordable and common **Kenyan dishes** that students love!

---

## ✨ Features
- 🤖 AI-powered chat interface with Streamlit
- 🥘 Intelligent meal suggestions based on ingredients, goals, and preferences
- 💰 Budget-friendly meal recommendations
- ⚖️ Weight loss/gain meal planning
- 🥗 Dietary restriction support (vegetarian, vegan, etc.)
- 🧠 Smart intent parsing and meal database
- 🌐 Web-based interface (no terminal required)

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
   streamlit run app.py
   ```

5. Open your browser and start chatting with DormChef AI!

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
