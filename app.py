import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import sqlite3
import json
import time

# Load environment variables
load_dotenv()

# Configure Google Generative AI
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the generative model
model = genai.GenerativeModel('gemini-1.5-pro')

conn = sqlite3.connect('chat_sessions.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS chat_sessions
             (id INTEGER PRIMARY KEY, session_name TEXT, history TEXT)''')
conn.commit()

# Streamlit app setup
st.set_page_config(page_title="RAG Study App", page_icon=":robot_face:")
st.title("Sad GPT")
st.write("Ask any question, and I'll provide a detailed explanation.")

# Initialize session state if not already done
if "selected_session" not in st.session_state:
    st.session_state["selected_session"] = None
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Function to save chat session
def save_chat_session(session_id, session_name, history):
    c.execute("UPDATE chat_sessions SET history=? WHERE id=?", (json.dumps(history), session_id))
    conn.commit()

# Function to rename a session
def rename_session(session_id, new_name):
    c.execute("UPDATE chat_sessions SET session_name=? WHERE id=?", (new_name, session_id))
    conn.commit()

# Function to delete a session
def delete_session(session_id):
    c.execute("DELETE FROM chat_sessions WHERE id=?", (session_id,))
    conn.commit()

# Function to get session ID
def get_session_id():
    return c.execute("SELECT id FROM chat_sessions WHERE session_name=?", (st.session_state.get("selected_session", ""),)).fetchone()

# Function to get session names
def get_session_names():
    return [row[1] for row in c.execute("SELECT * FROM chat_sessions")]

# Custom function to serialize the chat history
def serialize_history(history):
    return json.dumps(history)

# Custom function to deserialize the chat history
def deserialize_history(history_json):
    return json.loads(history_json)

# Load session chat history
def load_session_chat(session_state):
    if session_state["selected_session"]:
        c.execute("SELECT history FROM chat_sessions WHERE session_name=?", (session_state["selected_session"],))
        history_json = c.fetchone()
        if history_json:
            session_state['history'] = deserialize_history(history_json[0])
        else:
            session_state['history'] = []

# Sidebar for session management
session_names = get_session_names()
if st.sidebar.button("New Chat 🖋️"):
    st.session_state["selected_session"] = None
    st.session_state['history'] = []

st.sidebar.write("Select Session")
for session_name in session_names:
    if st.sidebar.button(session_name):
        st.session_state["selected_session"] = session_name
        load_session_chat(st.session_state)

if st.session_state["selected_session"]:
    st.write(f"Selected Session: {st.session_state['selected_session']}")
    session_id = get_session_id()
    if session_id:
        session_id = session_id[0]
        load_session_chat(st.session_state)

        with st.sidebar.expander("Session Actions"):
            new_session_name = st.text_input("Rename Session", value=st.session_state["selected_session"])
            if st.button("Rename") and new_session_name:
                rename_session(session_id, new_session_name)
                st.session_state["selected_session"] = new_session_name
                st.experimental_rerun()

            if st.button("Delete Session"):
                delete_session(session_id)
                st.session_state["selected_session"] = None
                st.session_state["history"] = []
                st.experimental_rerun()

# Display chat history
for message in st.session_state['history']:
    if message["role"] == "user":
        with st.chat_message("user", avatar="🧑"):
            st.write(message["parts"][0])
    else:
        with st.chat_message("model", avatar="🤖"):
            st.write(message["parts"][0])

# User input
user_input = st.text_input("Your question:", key="input")

# Handle user input
if st.button("Send") and user_input:
    user_message = {'role': 'user', 'parts': [user_input]}
    st.session_state['history'].append(user_message)

    # Create a placeholder for the model's response
    response_placeholder = st.empty()
    response_parts = []

    # Stream the response from the model
    prompt = st.session_state['history']
    response_generator = model.generate_content(prompt, stream=True)
    
    for response_part in response_generator:
        response_parts.append(response_part.text)
        response_placeholder.empty()
        with response_placeholder.container():
            with st.chat_message("model", avatar="🤖"):
                st.write("".join(response_parts))
        # Adding a small delay to simulate streaming, you might need to adjust or remove this
        time.sleep(0.01)

    model_message = {'role': 'model', 'parts': ["".join(response_parts)]}
    st.session_state['history'].append(model_message)

    session_id = get_session_id()
    if session_id:
        session_id = session_id[0]
        save_chat_session(session_id, st.session_state["selected_session"], st.session_state['history'])
    else:
        prompt = f'Provide a short and descriptive session name for this chat about "{user_input}". Return just one name only and nothing else.'
        new_session_name_response = model.generate_content(prompt)
        new_session_name = new_session_name_response.text.strip()
        c.execute("INSERT INTO chat_sessions (session_name, history) VALUES (?, ?)", (new_session_name, serialize_history(st.session_state['history'])))
        conn.commit()
        session_id = c.lastrowid
        st.session_state["selected_session"] = new_session_name

    st.experimental_rerun()
