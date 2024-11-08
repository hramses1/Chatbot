# message_state.py
import streamlit as st
from feature.chatbot.services.other_service import (
    get_specialties_message,
    get_list_options_message,
    get_interest_query_message
)

# Inicializa el historial de mensajes si no existe
def initialize_messages():
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            get_list_options_message(),
            get_specialties_message(),
            get_interest_query_message()
        ]

# Función para obtener el historial de mensajes
def get_messages():
    initialize_messages()
    return st.session_state.messages

# Función para agregar un mensaje al historial
def add_message(message):
    initialize_messages()
    st.session_state.messages.append(message)