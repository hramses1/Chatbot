from feature.chatbot.action.service.get_services_action import get_service_action
from feature.chatbot.services.other_service import get_service_details_message
from feature.chatbot.action.category.get_category_action import get_category_action
from feature.chatbot.view.message_state import initialize_messages, get_messages, add_message 

from difflib import get_close_matches


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


from difflib import get_close_matches

def classify_selection_service(texto: str):
    close_match = texto.strip().lower()
    normalized_name_area_selected = f"servicios de derecho {close_match}"
    
    # Obtener la categoría basada en el texto ingresado
    category = get_category_action(normalized_name_area_selected)
    
    if not category:
        return "No se encontró una Categoria coincidente.", False
    
    # Obtener la lista de servicios de la categoría encontrada
    services = get_service_action(category["id"])
    if not services:
        return "No se encontraron servicios disponibles.", False

    # Extraer los nombres de los servicios
    messages = [service['name'] for service in services if 'name' in service]
    
    # Obtener el último mensaje enviado
    last_message = get_messages()[-1]
    
    print("Servicios disponibles:", messages)
    print("Último mensaje:", last_message['text'])
    
    # Verificar si el último mensaje tiene una similitud con algún nombre de servicio
    similar_message = get_close_matches(last_message['text'], messages, n=1, cutoff=0.6)
    
    if similar_message:
        return similar_message[0], True

    return "No se encontró un mensaje similar.", False

