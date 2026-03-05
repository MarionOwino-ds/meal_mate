import streamlit as st
from chatbot import *

st.title("🍴 MealMate AI")


if "messages" not in st.session_state:
    st.session_state.messages = []


user_input = st.chat_input("What do you feel like eating?")


if user_input:

    st.session_state.messages.append(("You", user_input))

    response = ""

    if "lose weight" in user_input:
        meals = weight_loss_meals()
        response = random_response() + "\n\n" + "\n".join(meals)

    elif "cheap" in user_input or "budget" in user_input:
        meals = budget_meals()
        response = random_response() + "\n\n" + "\n".join(meals)

    else:

        words = user_input.split()

        suggestions = []

        for w in words:
            meals = get_meals_by_ingredient(w)
            suggestions.extend(meals)

        if suggestions:
            response = random_response() + "\n\n" + "\n".join(set(suggestions))
        else:
            response = "I'm not sure yet 😅 try telling me an ingredient."


    st.session_state.messages.append(("MealMate", response))


for role, message in st.session_state.messages:
    st.write(f"**{role}:** {message}")