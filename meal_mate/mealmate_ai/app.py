import streamlit as st
from chatbot import get_chatbot_response

# Page configuration
st.set_page_config(
    page_title="🍴 DormChef AI - Meal Recommendations",
    page_icon="🍴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        color: #2E8B57;
        margin-bottom: 1em;
    }
    .subtitle {
        font-size: 1.2em;
        text-align: center;
        color: #666;
        margin-bottom: 2em;
    }
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #e9ecef;
    }
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 12px 16px;
        border-radius: 18px;
        margin: 8px 0;
        max-width: 70%;
        float: right;
        clear: both;
    }
    .bot-message {
        background-color: #e9ecef;
        color: #333;
        padding: 12px 16px;
        border-radius: 18px;
        margin: 8px 0;
        max-width: 70%;
        float: left;
        clear: both;
    }
    .tips-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 15px;
        margin: 20px 0;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with instructions
with st.sidebar:
    st.title("🍴 DormChef AI")
    st.markdown("---")

    st.markdown("### 🎯 What I Can Help With:")
    st.markdown("• **Dietary Goals:** Weight loss/gain")
    st.markdown("• **Budget Meals:** Under KES 500")
    st.markdown("• **Ingredients:** What you have")
    st.markdown("• **Restrictions:** Vegetarian, vegan, etc.")
    st.markdown("• **Meal Types:** Breakfast, lunch, dinner")

    st.markdown("---")

    st.markdown("### 💡 Example Queries:")
    examples = [
        "I want to lose weight",
        "Cheap meals with chicken",
        "Vegetarian dinner ideas",
        "High calorie breakfast",
        "Meals with rice and beans"
    ]

    for example in examples:
        if st.button(f"💬 {example}", key=example):
            st.session_state.user_input = example
            st.rerun()

    st.markdown("---")
    st.markdown("### 📊 About")
    st.markdown("**DormChef AI** helps Kenyan students find affordable, healthy meals based on local ingredients and dietary preferences.")

# Main content
st.markdown('<h1 class="main-header">🍴 DormChef AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your intelligent meal recommendation assistant for Kenyan cuisine!</p>', unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add welcome message if this is the first interaction
if not st.session_state.messages:
    welcome_msg = """👋 **Hi there! I'm DormChef AI!**

I'm here to help you discover delicious Kenyan meals based on:
• Your dietary goals (weight loss/gain)
• Budget constraints (under KES 500)
• Available ingredients
• Dietary restrictions

**Try asking me things like:**
• "I want to lose weight"
• "Cheap meals with chicken"
• "Vegetarian dinner ideas"
• "What can I make with beans?"

What are you in the mood for today? 🍽️"""
    st.session_state.messages.append(("DormChef", welcome_msg))

# Display conversation in a styled container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for role, message in st.session_state.messages:
    if role == "DormChef":
        st.markdown(f'<div class="bot-message">🤖 **DormChef:**<br>{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-message">👤 **You:**<br>{message}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Clear floats
st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)

# Tips section
with st.expander("💡 Tips for Better Results", expanded=False):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🎯 Be Specific:**")
        st.markdown("• 'Low-calorie chicken dinner'")
        st.markdown("• 'Budget vegetarian lunch'")
        st.markdown("• 'Quick breakfast ideas'")

    with col2:
        st.markdown("**🥘 Use Keywords:**")
        st.markdown("• 'Cheap', 'healthy', 'quick'")
        st.markdown("• 'Vegetarian', 'vegan', 'gluten-free'")
        st.markdown("• 'Breakfast', 'lunch', 'dinner'")

# Chat input
user_input = st.chat_input("Ask me about meals, ingredients, or dietary goals...")

# Handle user input
if user_input:
    # Add user message
    st.session_state.messages.append(("You", user_input))

    # Get chatbot response
    with st.spinner("🤔 Thinking of the perfect meal recommendations..."):
        response = get_chatbot_response(user_input)

    # Add bot response
    st.session_state.messages.append(("DormChef", response))

    # Rerun to update the display
    st.rerun()

# Footer
st.markdown("---")
st.markdown("🍴 **DormChef AI** - Making healthy eating affordable and delicious for Kenyan students!")
st.markdown("*Built with Streamlit and powered by intelligent meal matching algorithms*")