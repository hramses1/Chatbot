# message_service.py
from feature.chatbot.services.specialty_service import classify_specialties
from feature.chatbot.services.category_service import classify_categories
from feature.chatbot.models.message_model import MessageModel
from feature.chatbot.view.message_state import initialize_messages, get_messages, add_message 
from feature.chatbot.view.form_user import activate_form_user,get_form_data_user
from feature.chatbot.services.services_service import classify_selection_service, classify_servicies
from feature.chatbot.utils.json_utils import save_to_json

class MessageService:
    
    def __init__(self, user_input: str):
        self.user_input = user_input

    def create_user_message(self) -> dict:
        """Crea y devuelve un mensaje de usuario."""
        user_message = MessageModel(sender="User", text=self.user_input)
        return {"sender": "user", "text": user_message.text}

    def generate_multiple_responses(self) -> list:
        """Genera múltiples respuestas del bot como una lista de mensajes."""
        responses = []
        last_message = get_messages()[-1]
        specialty, is_specialty_valid = classify_specialties(last_message['text'])
        print('is_specialty: ',specialty)
        if is_specialty_valid:
            classify_servicies(specialty)
            save_to_json(specialty)
        else:
            responses.append({"sender": "bot", "text": classify_selection_service()[0]})
            print(classify_selection_service()[0])
            activate_form_user()
        return responses
