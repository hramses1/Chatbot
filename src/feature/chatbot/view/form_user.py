import streamlit as st
from feature.chatbot.services.form_data_service import FormDataService

def show_form_user():
    """Formulario para recopilar información del usuario."""
    with st.form("Peticion de información"):
        nombre = st.text_input("Nombre")
        email = st.text_input("Email")
        identificacion = st.text_input("Identificación")
        
        enviar = st.form_submit_button("Enviar")
        if enviar:
            if nombre and email and identificacion:
                # Crear un diccionario con los datos del formulario
                form_data = {
                    'nombre': nombre,
                    'email': email,
                    'id': identificacion
                }
                
                # Ejecutar el servicio para procesar los datos
                form_service = FormDataService(form_data)
                form_service.process_form_data()

                # Restablecer el estado para evitar que el formulario se muestre de nuevo
                st.session_state['show_form_user'] = False
                st.rerun()
            else:
                st.error("Por favor, completa todos los campos.")


def get_form_data_user():
    return {
        'nombre': st.session_state.get('nombre', ''),
        'email': st.session_state.get('email', ''),
        'id': st.session_state.get('id', '')
    }

def activate_form_user():
    st.session_state['show_form_user'] = True
    
