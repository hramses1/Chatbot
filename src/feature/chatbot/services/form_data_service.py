import streamlit as st
from feature.chatbot.services.customer_service import process_form_submission
from feature.chatbot.utils.json_utils import save_to_json
import time

class FormDataService:
    def __init__(self, data: dict):
        """Inicializa el servicio con los datos proporcionados."""
        self.data = data

    def process_form_data(self):
        """Procesa los datos extraídos del formulario."""
        if self.data['nombre'] and self.data['email'] and self.data['id']:
            # Imprimir los datos en la consola
            print("Datos del formulario recibidos:", self.data)
            
            # Guardar los datos en un archivo JSON
            save_to_json(self.data)
            process_form_submission()
            
            # Mostrar un mensaje de éxito en la interfaz de usuario
            st.success(f"Gracias, {self.data['nombre']}. Tus datos han sido recibidos.")
            
            # Mostrar mensaje adicional indicando que la cita ha sido agendada
            st.success("🎉 Tu cita ha sido agendada exitosamente.")

            # Configurar un estado para retrasar el reinicio del chat
            st.session_state['appointment_confirmed'] = True
            
            # Esperar unos segundos antes de reiniciar el chat
            time.sleep(3)
            
            # Reiniciar el estado para que el chatbot comience desde el inicio
            self.reset_chat()

        else:
            st.error("Faltan datos en el formulario. Por favor, completa todos los campos.")

    def reset_chat(self):
        """Reinicia el estado del chatbot para comenzar desde el inicio."""
        st.session_state.clear()
        st.rerun()
