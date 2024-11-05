import streamlit as st

def chat_window(messages):
    for message in messages:
        if isinstance(message, dict) and message.get("sender") == "user":
            st.markdown(f"**🧑‍💼 Tú:** {message['text']}")
        elif isinstance(message, dict) and message.get("sender") == "bot":
            st.markdown(f"**🤖 Bot:** {message['text']}")
        else:
            st.write(message)
