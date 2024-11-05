# main.py
import streamlit as st
from config.config import APP_NAME
from feature.chatbot.view.chatbot_view import display_chatbot

def main():
    st.title(APP_NAME)
    display_chatbot()

if __name__ == "__main__":
    main()
