import streamlit as st
from feature.chatbot.services.customer_service import process_form_submission
from feature.chatbot.services.other_service import create_custom_message
from feature.chatbot.services.ws_service import send_message_service
from feature.chatbot.utils.json_utils import get_all_data_from_json, save_to_json
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
            time.sleep(3)
            data = get_all_data_from_json()
            estimated_time = data.get("appointment_timing")
            status_appointment = data.get("status_appointment")
            
            response = send_message_service(
            to=f"+593{self.data['telefono']}",
            message_type="simple",
            message=create_custom_message(self.data, estimated_time ) )
            
            print("Respuesta:", response)

            if not status_appointment:
                st.success(f"Bienvenido de nuevo, {self.data['nombre']}. Tus datos han sido recibidos.")
            else:
                st.success(f"Gracias, {self.data['nombre']}. Tus datos han sido recibidos.")

            # Mostrar mensaje adicional indicando que la cita ha sido agendada
            st.success(f"🎉 Tu cita ha sido agendada exitosamente para: {estimated_time['start_time']} ")

            # Mostrar mensaje adicional para recordar al usuario revisar su correo electrónico
            st.info("📧 Por favor, revisa tu correo electrónico para aceptar la invitación a la reunión. Si no la encuentras, revisa también tu carpeta de spam o correo no deseado.")
            
            st.info("⏱️ En 10 segundos volvera al inicio, Muchas gracias por usar nuestro servicio!.")
            # Configurar un estado para retrasar el reinicio del chat
            st.session_state['appointment_confirmed'] = True
            
            # Esperar unos segundos antes de reiniciar el chat
            time.sleep(10)
            
            # Reiniciar el estado para que el chatbot comience desde el inicio
            self.reset_chat()

        else:
            st.error("Faltan datos en el formulario. Por favor, completa todos los campos.")

    def reset_chat(self):
        """Reinicia el estado del chatbot para comenzar desde el inicio."""
        st.session_state.clear()
        st.rerun()
