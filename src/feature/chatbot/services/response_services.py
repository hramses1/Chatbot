from feature.chatbot.services.specialty_service import classify_specialties
from feature.chatbot.services.category_service import classify_categories
from feature.chatbot.models.message_model import MessageModel
from feature.chatbot.view.message_state import get_messages, add_message
from feature.chatbot.view.form_user import activate_form_user
from feature.chatbot.services.services_service import classify_selection_service, classify_servicies
from feature.chatbot.utils.json_utils import save_to_json
import streamlit as st
class MessageService:
    def __init__(self, user_input: str):
        self.user_input = user_input

    def create_user_message(self) -> dict:
        """Crea y devuelve un mensaje de usuario."""
        user_message = MessageModel(sender="User", text=self.user_input)
        return {"sender": "user", "text": user_message.text}

    def generate_multiple_responses(self) -> list:
        """Genera múltiples respuestas del bot."""
        responses = []
        last_message_text = self.get_last_user_message()
        
        # Verificar si estamos esperando una respuesta de confirmación
        if st.session_state.get('awaiting_confirmation', False):
            self.handle_user_confirmation(responses)
        else:
            # Clasificar la especialidad si no estamos esperando confirmación
            specialty, is_specialty_valid = classify_specialties(last_message_text)
            if is_specialty_valid:
                self.handle_specialty(specialty, responses)
            else:
                self.handle_selection(responses)
        
        return responses

    def get_last_user_message(self) -> str:
        """Obtiene el texto del último mensaje del usuario."""
        messages = get_messages()
        return messages[-1]['text'] if messages else ""

    def handle_specialty(self, specialty: str, responses: list):
        """Maneja la lógica cuando se detecta una especialidad válida."""
        classify_servicies(specialty)
        save_to_json({"area": specialty})
        responses.append(f"Hemos identificado tu interés en: {specialty}.")

    def handle_selection(self, responses: list):
        """Maneja la lógica cuando no se detecta una especialidad válida."""
        selection, is_selection_valid = classify_selection_service()
        save_to_json({"is_selection_valid": is_selection_valid})

        # Si la selección es válida, preguntar si el usuario quiere ser contactado
        if is_selection_valid:
            # Guardar en el estado de sesión que estamos esperando una respuesta de confirmación
            st.session_state['awaiting_confirmation'] = True
            responses.append("¿Estás de acuerdo en que agendemos la cita? (Responde 'sí' o 'no')")
        else:
            responses.append(selection)
        
    def handle_user_confirmation(self, responses: list):
        """Maneja la respuesta del usuario a la confirmación de contacto."""
        user_input = self.user_input.lower()

        # Verificar si estamos esperando una confirmación y si la respuesta es 'sí'
        if st.session_state.get('awaiting_confirmation', False):
            if user_input in ['sí', 'si', 's', 'yes']:
                activate_form_user()
                responses.append("Perfecto, se te agendara la cita. Completa el formulario.")
            else:
                responses.append("Entendido, si necesitas algo más, estamos aquí para ayudarte.")
            
            # Resetear el estado de confirmación
            st.session_state['awaiting_confirmation'] = False
