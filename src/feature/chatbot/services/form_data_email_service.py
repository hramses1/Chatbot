import streamlit as st
from feature.chatbot.action.customer.get_customer_action import get_customer_action
import time
from jinja2 import Template
from feature.chatbot.action.view.get_service_user_view_action import get_customer_state_cases
from feature.chatbot.services.email_service import EmailService
from feature.chatbot.services.render_email_service import RenderService

class FormDataEmailService:
    def __init__(self, data: dict):
        """Inicializa el servicio con los datos proporcionados."""
        self.data = data

    def process_form_data_Email(self):
        """Procesa los datos extraídos del formulario."""
        if self.data['email']:
            # Imprimir los datos en la consola
            result_user = get_customer_action(self.data["email"])
            if result_user:
                # Obtener casos del cliente
                data_cases = get_customer_state_cases(self.data["email"])
                # Renderizar la plantilla con los datos
                html_content = RenderService.render_template(data_cases,result_user[0])

                # Enviar el correo
                email_service = EmailService()
                email_service.send_email(
                    to_email=self.data["email"],
                    subject="Resumen de Casos",
                    html_template=html_content,
                )

                st.success(f"Bienvenido de nuevo, {result_user[0]['nombre']}. Tus datos han sido enviados el correo: {self.data['email']}.")
                    # Mostrar mensaje adicional para recordar al usuario revisar su correo electrónico
                st.info("📧 Por favor, revisa tu correo electrónico para poder revisar tus seguimientos. Si no la encuentras, revisa también tu carpeta de spam o correo no deseado.")
            
                st.info("⏱️ En 10 segundos volvera al inicio, Muchas gracias por usar nuestro servicio!.")
                print()
            else:
                st.error("No se encontro el usuario con el email ingresado. Para que seas registrado tienes que agendar una cita.")
                return
            
            time.sleep(3)
            
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
