import streamlit as st
from feature.chatbot.utils.json_utils import clear_json
from feature.chatbot.services.other_service import (
    get_specialties_message,
    get_interest_query_message
)

def initialize_messages():
    """Inicializa el historial de mensajes si no existe."""
    if 'messages' not in st.session_state:
        clear_json()
        st.session_state.messages = [
            get_specialties_message(),
            get_interest_query_message()
        ]

def get_messages():
    """Obtiene el historial de mensajes."""
    initialize_messages()
    return st.session_state.messages

def add_message(message):
    """Agrega un mensaje al historial."""
    initialize_messages()
    # Validar que el mensaje sea un diccionario con las claves correctas
    if isinstance(message, dict) and "sender" in message and "text" in message:
        st.session_state.messages.append(message)

def display_messages():
    """Muestra los mensajes en el contenedor dinámicamente."""
    messages = get_messages()
    message_container = st.container()
    with message_container:
        for msg in messages:
            if isinstance(msg, dict):
                st.markdown(f"🗨️ {msg['text']}")
