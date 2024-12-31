import streamlit as st
import requests
import time

# Initialize session state variables for storing chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Function to send user message to the Rasa server and get a response
def get_bot_response(user_input):
    try:
        rasa_url = "http://localhost:5005/webhooks/rest/webhook"
        headers = {"Content-Type": "application/json"}
        data = {"sender": "user", "message": user_input}

        response = requests.post(rasa_url, json=data, headers=headers)
        if response.status_code == 200:
            bot_responses = response.json()
            if bot_responses:
                # Concatenate all bot responses
                bot_reply = "<br>".join([resp.get("text", "") for resp in bot_responses])
                return bot_reply if bot_reply else "No response from the bot."
            else:
                return "The bot did not return a response. Please try again."
        else:
            return f"Server error: {response.status_code}. Check if Rasa server is running."
    except requests.exceptions.ConnectionError:
        return "Unable to connect to the Rasa server. Is it running?"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# Streamlit UI setup
st.set_page_config(page_title="Learning Chatbot", page_icon="🤖", layout="wide")
st.title("🌟 Ask the Learning Bot 🌟")

# Sidebar
st.sidebar.title("🎓 Your Learning Companion")
st.sidebar.write("""
    - Looking for learning resources?
    - Get book recommendations!
    - Ask the bot for insightful explanations!
    - Enhance your knowledge in various fields.
    - Let the bot guide your learning journey!
""")

# Input field for user message
user_input = st.text_input("Type your message here 👇", placeholder="e.g., Tell me about Python programming", key="user_input")

# Send button to submit the user input
if st.button("Send"):
    if user_input.strip():
        with st.spinner('Thinking...'):
            # Get bot response
            bot_response = get_bot_response(user_input)
            
            # Append user input and bot response to chat history
            st.session_state.chat_history.append(f'<p class="user-message">You: {user_input}</p>')
            st.session_state.chat_history.append(f'<p class="bot-message">Bot: {bot_response}</p>')
    else:
        st.warning("Please enter a message before clicking Send.")

# Display chat history
chat_display = "".join(st.session_state.chat_history)

st.markdown(f"""
    <div class="chatbox">{chat_display}</div>
    <style>
        .chatbox {{
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            max-height: 400px;
            overflow-y: auto;
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }}
        .user-message {{ color: #004d8c; font-weight: bold; margin-bottom: 10px; }}
        .bot-message {{ color: #4caf50; font-weight: bold; margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# Automatically scroll down to show the latest messages
st.markdown("""
    <script>
        var chatbox = document.querySelector('.chatbox');
        if (chatbox) chatbox.scrollTop = chatbox.scrollHeight;
    </script>
""", unsafe_allow_html=True)
