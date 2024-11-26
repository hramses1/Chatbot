import streamlit as st
from feature.chatbot.components.chatbot_window import chat_window
from feature.chatbot.services.response_services import MessageService
from feature.chatbot.services.other_service import get_welcome_message
from feature.chatbot.view.form_email import show_form_email
from feature.chatbot.view.message_state import get_messages, add_message
from feature.chatbot.view.form_user import show_form_user

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
            
            # Verificar si se debe activar el formulario
            if bot_response.get("activate_form", False):
                st.session_state['show_form_user'] = True
                st.rerun() # Forzar la recarga para que el formulario aparezca inmediatamente

            render_chat()

    render_chat()  # Renderizar el chat al cargar la página

    # Mostrar el formulario de entrada de usuario o el formulario de contacto
    if st.session_state.get('show_form_user', False):
        show_form_user()
    if st.session_state.get('show_form_email', False):
        show_form_email()    
        
    else:
        with st.form(key='user_input_form', clear_on_submit=True):
            st.text_input("Tu:", key='user_input', placeholder="Escribe un mensaje...")
            if st.form_submit_button("Enviar"):
                handle_user_input()
                render_chat()