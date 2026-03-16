import streamlit as st
from chatbot import get_chatbot_response

st.title("🍴 MealMate AI")
st.write("Your friendly meal recommendation assistant! Tell me what you're craving or your dietary goals.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Add a welcome message if this is the first interaction
if not st.session_state.messages:
    st.session_state.messages.append(("MealMate", "Hi there! 👋 I'm here to help you find delicious meals. What are you in the mood for? You can tell me about ingredients, dietary goals, or budget preferences!"))

user_input = st.chat_input("What do you feel like eating?")

if user_input:
    # Add user message
    st.session_state.messages.append(("You", user_input))

    # Get chatbot response using the new intelligent system
    response = get_chatbot_response(user_input)

    # Add bot response
    st.session_state.messages.append(("MealMate", response))

# Display conversation
for role, message in st.session_state.messages:
    if role == "MealMate":
        st.markdown(f"**🤖 {role}:** {message}")
    else:
        st.markdown(f"**👤 {role}:** {message}")

# Add some helpful tips at the bottom
st.markdown("---")
st.markdown("💡 **Tips:** Try asking things like:")
st.markdown("- 'I want to lose weight'")
st.markdown("- 'Cheap meals with chicken'")
st.markdown("- 'High calorie breakfast ideas'")
st.markdown("- 'Budget-friendly dinner options'")