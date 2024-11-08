import streamlit as st
from feature.chatbot.components.chatbot_window import chat_window
from feature.chatbot.services.response_services import MessageService
from feature.chatbot.services.other_service import get_welcome_message
from feature.chatbot.view.message_state import initialize_messages, get_messages, add_message
from feature.chatbot.view.form_user import show_form_user
from feature.chatbot.utils.json_utils import clear_json


def display_chatbot():
    
    # Inicializar 'show_form' en False si no está definido
    if 'show_form_user' not in st.session_state:
        st.session_state['show_form_user'] = False

    # Inicializar mensajes en el estado de sesión
    initialize_messages()

    # Mostrar el mensaje de bienvenida
    st.write(get_welcome_message())

    # Mostrar historial de mensajes
    chat_window(get_messages())

    # Definir la función handle_user_input antes de usarla
    def handle_user_input():
        user_input = st.session_state.user_input
        if user_input:
            message_service = MessageService(user_input)
            # Agregar mensaje del usuario al historial
            add_message(message_service.create_user_message())
            # Obtener y agregar múltiples respuestas del bot
            with st.spinner("El bot está pensando..."):
                bot_responses = message_service.generate_multiple_responses()
                for response in bot_responses:
                    add_message(response)
            # Limpiar el campo de entrada
            st.session_state.user_input = ''

    # Controlar si mostrar el formulario o el campo de entrada
    if st.session_state.get('show_form_user', False):
        # Mostrar el formulario
        show_form_user()
        
    else:
        # Campo de entrada con callback
        st.text_input(
            "Tu:",
            key='user_input',
            placeholder="Escribe un mensaje...",
            on_change=handle_user_input
        )
