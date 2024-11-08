import streamlit as st

def show_form_user():
    with st.form("Peticion de información"):
        nombre = st.text_input("Nombre")
        email = st.text_input("Email")
        identificacion = st.text_input("Identificación")
        
        enviar = st.form_submit_button("Enviar")
        if enviar:
            if nombre and email and identificacion:
                # Guardar los datos en st.session_state
                st.session_state['nombre'] = nombre
                st.session_state['email'] = email
                st.session_state['id'] = identificacion
                # Restablecer la bandera para que el formulario no se muestre nuevamente
                st.session_state['show_form_user'] = False
                # Forzar reejecución del script
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
    
