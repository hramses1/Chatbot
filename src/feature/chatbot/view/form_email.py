import re
import streamlit as st
from feature.chatbot.services.form_data_email_service import FormDataEmailService
from feature.chatbot.services.form_data_service import FormDataService

# Función para validar email
def is_valid_email(email):
    """Valida que el email tenga un formato correcto."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def show_form_email():
    """Formulario para petición de EMAIL."""
    
    with st.form("Petición de información Email"):
        email = st.text_input("Email")
        enviar = st.form_submit_button("Enviar")
        
        if enviar:
            if email:
                if is_valid_email(email):
                    # Crear un diccionario con los datos del formulario
                    form_data = {'email': email}
                    
                    # Ejecutar el servicio para procesar los datos
                    form_service = FormDataEmailService(form_data)
                    form_service.process_form_data_Email()
                    
                    # Restablecer el estado para evitar que el formulario se muestre de nuevo
                    st.session_state['show_form_email'] = False
                    st.rerun()
                else:
                    st.error("Por favor, ingresa un email válido.")
            else:
                st.error("Por favor, completa todos los campos.")

def get_form_data_user():
    return {
        'email': st.session_state.get('email', ''),
    }

def activate_form_email():
    st.session_state['show_form_email'] = True
