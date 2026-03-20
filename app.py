import streamlit as st
from modules.auth import register_user, login_user
from modules.chatbot import get_response
from modules.history import (
    save_chat,
    get_current_chat,
    get_all_chats,
    new_chat,
    init_history
)

st.set_page_config(page_title="🤖 AI-NEXUS-chatbot", layout="wide")



def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user = None

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    
    init_history()



def login_page():
    st.markdown("<h1 style='text-align:center;'>AI Chatbot</h1>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

   
    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            success, user = login_user(email, password)

            if success:
                st.session_state.authenticated = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error(user)

   
    with tab2:
        name = st.text_input("Full Name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register"):
            success, msg = register_user(name, email, password)

            if success:
                st.success(msg)
            else:
                st.error(msg)



def chat_page():
    st.sidebar.write(f"Welcome {st.session_state.user['fullname']}")

   
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.chat_messages = []
        st.rerun()

 
    if st.sidebar.button("➕ New Chat"):
        new_chat()
        st.session_state.chat_messages = []
        st.rerun()

    st.sidebar.markdown("## Chat History")

    chats = get_all_chats()

 
    for chat_id, messages in chats.items():
        if messages:
            title = messages[0]["prompt"][:30]

            if st.sidebar.button(title, key=chat_id):
                st.session_state.current_chat_id = chat_id

          
                st.session_state.chat_messages = []
                for m in messages:
                    st.session_state.chat_messages.append(("user", m["prompt"]))
                    st.session_state.chat_messages.append(("ai", m["response"]))

                st.rerun()


    st.markdown("<h2 style='text-align:center;'>Ask anything</h2>", unsafe_allow_html=True)


    prompt = st.chat_input("Type your message...")

    if prompt:
       
        st.session_state.chat_messages.append(("user", prompt))

        with st.spinner("Thinking..."):
            response = get_response(prompt, get_current_chat())

       
        st.session_state.chat_messages.append(("ai", response))
        save_chat(prompt, response)

        st.rerun()

    
    for role, message in st.session_state.chat_messages:
        if role == "user":
            st.markdown(f"🧑 **You:** {message}")
        else:
            st.markdown(f"🤖 **AI:** {message}")

        st.markdown("---")



def main():
    init_session()

    if not st.session_state.authenticated:
        login_page()
        return

    chat_page()


if __name__ == "__main__":
    main()