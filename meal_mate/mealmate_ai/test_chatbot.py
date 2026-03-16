#!/usr/bin/env python3
"""
Test script for the improved MealMate chatbot
"""

from chatbot import get_chatbot_response, parse_user_intent, get_meals_by_criteria

def test_chatbot():
    """Test various chatbot inputs"""

    test_cases = [
        "I want to lose weight",
        "cheap meals with chicken",
        "high calorie breakfast ideas",
        "budget-friendly dinner options",
        "meals with rice and beans",
        "breakfast options",
        "something for lunch",
        "dinner ideas",
        "vegetarian meals",
        "I need to gain weight"
    ]

    print("🧪 Testing MealMate Chatbot Improvements\n")
    print("=" * 50)

    for i, test_input in enumerate(test_cases, 1):
        print(f"\nTest {i}: '{test_input}'")
        print("-" * 30)

        # Show parsed intent
        intent = parse_user_intent(test_input)
        print(f"Parsed Intent: {intent}")

        # Get response
        response = get_chatbot_response(test_input)
        print(f"Response: {response[:200]}..." if len(response) > 200 else f"Response: {response}")
        print()

if __name__ == "__main__":
    test_chatbot()