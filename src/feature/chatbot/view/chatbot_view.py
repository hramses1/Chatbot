import streamlit as st
from feature.chatbot.components.chatbot_window import chat_window
from feature.chatbot.services.response_services import MessageService
from feature.chatbot.services.other_service import get_welcome_message
from feature.chatbot.view.message_state import get_messages, add_message
from feature.chatbot.view.form_user import show_form_user

def display_chatbot():
    """Función principal para mostrar el chatbot."""

    # Inicializar estados si no están definidos
    if 'show_form_user' not in st.session_state:
        st.session_state['show_form_user'] = False

    if 'welcome_shown' not in st.session_state:
        st.session_state['welcome_shown'] = True
        st.write(get_welcome_message())

    # Contenedor dinámico para actualizar el chat en tiempo real
    chat_container = st.empty()

    def render_chat():
        """Renderiza la ventana de chat con desplazamiento automático."""
        with chat_container.container():
            chat_window(get_messages())
            # Forzar el scroll al final de la página para mostrar el último mensaje
            st.write("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)

    render_chat()

    def handle_user_input():
        """Procesa la entrada del usuario y genera la respuesta del bot."""
        user_input = st.session_state.user_input
        if user_input:
            message_service = MessageService(user_input)
            user_message = {"sender": "user", "text": user_input}

            add_message(user_message)
            render_chat()  # Mostrar mensaje inmediatamente

            with st.spinner("El bot está pensando..."):
                bot_responses = message_service.generate_multiple_responses()
                for response in bot_responses:
                    bot_message = {"sender": "bot", "text": response}
                    add_message(bot_message)
                render_chat()  # Actualizar el chat después de la respuesta

    # Mostrar el formulario de entrada de usuario
    if st.session_state.get('show_form_user', False):
        show_form_user()
    else:
        with st.form(key='user_input_form', clear_on_submit=True):
            st.text_input("Tu:", key='user_input', placeholder="Escribe un mensaje...")
            submitted = st.form_submit_button("Enviar")
            if submitted:
                handle_user_input()
                render_chat()

