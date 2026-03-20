import streamlit as st
import uuid


def init_history():
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}

    if "current_chat_id" not in st.session_state:
        new_chat()


def new_chat():
    chat_id = str(uuid.uuid4())
    st.session_state.chat_sessions[chat_id] = []
    st.session_state.current_chat_id = chat_id


def save_chat(prompt, response):
    chat_id = st.session_state.current_chat_id

    st.session_state.chat_sessions[chat_id].append({
        "prompt": prompt,
        "response": response
    })


def get_current_chat():
    return st.session_state.chat_sessions[st.session_state.current_chat_id]


def get_all_chats():
    return st.session_state.chat_sessions