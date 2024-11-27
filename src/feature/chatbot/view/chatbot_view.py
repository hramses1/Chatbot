import streamlit as st
from feature.chatbot.components.chatbot_window import chat_window
from feature.chatbot.services.response_services import MessageService
from feature.chatbot.services.other_service import get_welcome_message
from feature.chatbot.view.form_email import show_form_email
from feature.chatbot.view.message_state import get_messages, add_message
from feature.chatbot.view.form_user import show_form_user
from dotenv import load_dotenv
import os

load_dotenv()

def display_chatbot():
    """Función principal para mostrar el chatbot."""

    # Inicializar estados si no están definidos
    if 'show_form_user' not in st.session_state:
        st.session_state['show_form_user'] = False

    if 'show_form_email' not in st.session_state:
        st.session_state['show_form_email'] = False

    if 'welcome_shown' not in st.session_state:
        st.session_state['welcome_shown'] = True
        st.markdown(f"### {get_welcome_message()}")

    # Contenedor dinámico para actualizar el chat en tiempo real
    chat_container = st.empty()

    def render_chat():
        """Renderiza la ventana de chat con desplazamiento automático."""
        with chat_container.container():
            chat_window(get_messages())

    def handle_user_input():
        """Procesa la entrada del usuario y genera la respuesta del bot."""
        user_input = st.session_state.user_input
        if user_input:
            user_message = {"sender": "user", "text": user_input}
            add_message(user_message)
            render_chat()

            # Generar respuestas del bot
            message_service = MessageService(user_input)
            bot_response = message_service.generate_multiple_responses()

            # Asegurarse de que bot_response sea un diccionario antes de acceder
            if isinstance(bot_response, dict) and "responses" in bot_response:
                for response in bot_response["responses"]:
                    if response:
                        bot_message = {"sender": "bot", "text": response}
                        add_message(bot_message)

            # Verificar si se debe activar algún formulario
            if bot_response.get("activate_form", "user") == "user":
                set_active_form("show_form_user")
            elif bot_response.get("activate_form", "email") == "email":
                set_active_form("show_form_email")

            render_chat()

    def set_active_form(form_name):
        """Asegura que solo un formulario esté activo a la vez."""
        st.session_state['show_form_user'] = form_name == 'show_form_user'
        st.session_state['show_form_email'] = form_name == 'show_form_email'
        st.rerun()

    render_chat()  # Renderizar el chat al cargar la página

    # Mostrar el formulario correspondiente
    if st.session_state['show_form_user']:
        show_form_user()
    elif st.session_state['show_form_email']:
        show_form_email()
    else:
        with st.form(key='user_input_form', clear_on_submit=True):
            st.text_input("Tu:", key='user_input', placeholder="Escribe un mensaje...")
            col1, col2 = st.columns([3, 1])  # Crear dos columnas para los botones

            with col1:
                if st.form_submit_button("Enviar"):
                    handle_user_input()
            
            with col2:
                if st.form_submit_button("Volver a la landing"):
                    # Obtener la URL de la landing desde las variables de entorno
                    landing_url = os.getenv("LANDING_PAGE_URL")

                    # Mostrar un mensaje al usuario
                    st.success("Redirigiéndote a la página principal...")

                    # Redirigir inmediatamente utilizando HTML
                    st.markdown(
                        f"""
                        <meta http-equiv="refresh" content="0; url={landing_url}">
                        <noscript>
                            <div style="margin-top: 20px;">
                                Si no eres redirigido automáticamente, haz clic en este enlace: 
                                <a href="{landing_url}">Ir a la página principal</a>
                            </div>
                        </noscript>
                        """,
                        unsafe_allow_html=True
                    )