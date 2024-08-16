import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize generative AI model
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to get response from the model
def get_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return "Sorry, I couldn't process that request."

# Streamlit interface setup
st.set_page_config(page_title="Simple ChatBot!", layout='centered')
st.title("Chat-Bot")
st.write("Powered by Google.")

# Initialize session state to save chat history
if 'history' not in st.session_state:
    st.session_state.history = []

# Chat form
with st.form(key="chat-form", clear_on_submit=True):
    prompt = st.text_input("Enter your message:", max_chars=2000)
    submit_button = st.form_submit_button("Send")

    if submit_button:
        if prompt:
            response = get_response(prompt)
            # Save the prompt and response to the session state history
            st.session_state.history.append({"user": prompt, "bot": response})
        else:
            st.warning("Please enter a prompt.")

# Display chat history
if st.session_state.history:
    st.write("### Chat History")
    for chat in st.session_state.history:
        st.write(f"**You:** {chat['user']}")
        st.write(f"**Bot:** {chat['bot']}")
