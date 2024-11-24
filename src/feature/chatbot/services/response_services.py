from feature.chatbot.handlers.classification_handler import handle_classification
from feature.chatbot.handlers.confirmation_handler import handle_user_confirmation
from feature.chatbot.handlers.option_handle import handle_option_selection
from feature.chatbot.services.intent_service import detect_intent
from feature.chatbot.handlers.case_handler import handle_case_review
from feature.chatbot.services.other_service import handle_schedule_appointment
import streamlit as st

class MessageService:
    def __init__(self, user_input: str):
        self.user_input = user_input.lower().strip()

    def create_user_message(self) -> dict:
        """Crea y devuelve un mensaje de usuario."""
        return {"sender": "user", "text": self.user_input}

    def generate_multiple_responses(self) -> dict:
        """Genera respuestas del bot y devuelve un diccionario."""
        responses = []

        # Detectar intención principal
        intent = detect_intent(self.user_input)
        if intent == "schedule_appointment":
            responses.extend(handle_schedule_appointment())
            return {"responses": responses, "activate_form": False}

        elif intent == "review_cases":
            responses.extend(handle_case_review())
            return {"responses": responses, "activate_form": False}

        # Continuar con el flujo normal si no se detecta una intención específica
        if st.session_state.get("awaiting_confirmation", False):
            handle_user_confirmation(self.user_input,responses)
        elif st.session_state.get("awaiting_option_selection", False):
            handle_option_selection(responses)
        else:
            handle_classification(self.user_input, responses)

        return {
            "responses": responses,
            "activate_form": st.session_state.get("show_form_user", False),
        }
