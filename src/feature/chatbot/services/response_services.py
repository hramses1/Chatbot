from feature.chatbot.services.specialty_service import classify_specialties
from feature.chatbot.services.category_service import classify_categories
from feature.chatbot.models.message_model import MessageModel


# feature/chatbot/services/message_services.py
class MessageService():
    
    def __init__(self,input: str):
        self.__input = input
    
    def create_user_message (self,user_input: str) -> dict:
        user_message = MessageModel(sender="User", text=user_input)
        user_message_data = {"sender": "user", "text": user_message.text}
        return user_message_data

    def generate_bot_response(self) -> dict:
        self.get_response_service()
        bot_response_text = self.__input
        bot_message_data = {"sender": "bot", "text": bot_response_text}
        return bot_message_data

    def get_response_service(self):
        
        message_specialty = classify_specialties(self.__input)[0]
        condition_specialty = classify_specialties(self.__input)[1]
        message_category = ''
        condition_category = ''
        self.__input = message_specialty
        if condition_specialty:
            message_category = classify_categories(message_specialty)
            condition_category = message_category[1]
            self.__input = message_category[0]
            
            if condition_category:
                self.__input = "Las opciones disponibles son: 'especialidades', 'consulta de interés'"
    
    
    # if condition_category:
    #     return generate_bot_response('¿En cuál de estas áreas te gustaría consultar y agendar una cita? Selecciona la que más se ajuste a lo que necesitas, y te ayudaremos a coordinar tu cita lo antes posible. 😊')
    
    # if input == "listar opciones":
    #     return generate_bot_response("Las opciones disponibles son: 'especialidades', 'consulta de interés'")
    
    # return generate_bot_response(message_specialty)
