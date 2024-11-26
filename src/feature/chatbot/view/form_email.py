import streamlit as st
from feature.chatbot.services.form_data_email_service import FormDataEmailService
from feature.chatbot.services.form_data_service import FormDataService

def show_form_email():
    """Formulario para peticion de EMAIL."""
    
    with st.form("Peticion de información Email"):
        email = st.text_input("Email")
        enviar = st.form_submit_button("Enviar")
        if enviar:
            if email:
                # Crear un diccionario con los datos del formulario
                form_data = {
                    'email': email,
                }
                
                # Ejecutar el servicio para procesar los datos
                form_service = FormDataEmailService(form_data)
                form_service.process_form_data_Email()

                # Restablecer el estado para evitar que el formulario se muestre de nuevo
                st.session_state['show_form_email'] = False
                st.rerun()
            else:
                st.error("Por favor, completa todos los campos.")


def get_form_data_user():
    return {
        'email': st.session_state.get('email', ''),
    }

def activate_form_email():
    st.session_state['show_form_email'] = True
    
