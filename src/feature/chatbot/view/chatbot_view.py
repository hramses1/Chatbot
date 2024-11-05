# Archivo principal

import streamlit as st
from feature.chatbot.components.chatbot_window import chat_window
from feature.chatbot.services.response_services import MessageService
from feature.chatbot.services.other_service import get_welcome_message, get_specialties_message, get_list_options_message, get_interest_query_message

# Función de callback para procesar la entrada del usuario y limpiar el campo
def handle_user_input():
    user_input = st.session_state.user_input
    messageService = MessageService(user_input)
    if user_input:
        # Procesar y enviar mensaje usando el servicio
        with st.spinner("El bot está pensando..."):
            st.session_state.messages.append(messageService.create_user_message(user_input))
            st.session_state.messages.append(messageService.generate_bot_response())

        # Limpiar el campo de entrada
        st.session_state.user_input = ""  # Esto limpia el texto ingresado

def display_chatbot():
    st.write(get_welcome_message())

    if "initialized" not in st.session_state:
        with st.spinner("Cargando..."):
            st.session_state.messages = [
                get_list_options_message(),
                get_specialties_message(),
                get_interest_query_message()
            ]
            st.session_state.initialized = True
                
    # Mostrar historial de mensajes
    chat_window(st.session_state.messages)

    # Campo de entrada con callback para manejar el mensaje
    st.text_input("Tu:", key="user_input", placeholder="Escribe un mensaje...", on_change=handle_user_input)
