from feature.chatbot.action.service.get_services_action import get_service_action
from feature.chatbot.services.other_service import get_service_details_message

def classify_servicies(id: str):
    services = get_service_action(id)
    if services:
        messages = []
        for service in services:
            message = get_service_details_message(service)  # Llama uno por uno
            messages.append(message)
        return "\n".join(messages), True  # Une todos los mensajes en una sola respuesta
    else:
        return "No se encontró un servicio coincidente.", False

