from feature.chatbot.handlers.classification_handler import handle_classification
from feature.chatbot.handlers.confirmation_handler import handle_user_confirmation
from feature.chatbot.handlers.option_handle import handle_option_selection
from feature.chatbot.services.intent_service import detect_intent
from feature.chatbot.handlers.case_handler import handle_case_review
from feature.chatbot.services.other_service import handle_schedule_appointment
import streamlit as st

from feature.chatbot.utils.json_utils import get_all_data_from_json
from feature.chatbot.utils.json_utils import clear_json

class MessageService:
    def __init__(self, user_input: str):
        self.user_input = user_input.lower().strip()

    def create_user_message(self) -> dict:
        """Crea y devuelve un mensaje de usuario."""
        return {"sender": "user", "text": self.user_input}

    def generate_multiple_responses(self) -> dict:
        """Genera respuestas del bot y devuelve un diccionario."""
        responses = []
        data = get_all_data_from_json()
        
        area_is_valid = data.get("area")
        # Detectar intención principal
        valid=detect_intent(self.user_input)
        intent = data.get("state_chat") or valid
        if intent == "schedule_appointment" or area_is_valid:
            if valid is not None and not area_is_valid:
                responses.append(handle_schedule_appointment())
            
            if st.session_state.get("awaiting_confirmation", False):
                handle_user_confirmation(self.user_input,responses)
            
            elif st.session_state.get("awaiting_option_selection", False):
                handle_option_selection(responses)
            
            if valid is None and not area_is_valid:
                handle_classification(self.user_input, responses)
            
            if valid is not None and area_is_valid:
                clear_json()
            
            return {
                "responses": responses,
                "activate_form": st.session_state.get("show_form_user", False),
            }

        elif intent == "review_cases":
            responses.extend(handle_case_review())
            return {"responses": responses, "show_form_email": True}
        
        else:
            return {
                "responses":{
                    "Lo siento, no entendí tu mensaje. Por favor, elige una de estas opciones: 'Agendar cita' o 'Revisar casos'."},
                    "activate_form": st.session_state.get("show_form_user", False),
                
            }

