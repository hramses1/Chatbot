from feature.chatbot.action.category.get_category_action import get_category_action
from feature.chatbot.services.services_service import classify_servicies

def classify_categories(texto: str):
    close_match = texto.strip().lower()
    normalized_name_area_selected = f"servicios de derecho {close_match}"
    category = get_category_action(normalized_name_area_selected)
    message_service = classify_servicies(category["id"])[0]
    
    if category:
        return message_service, True
    else:
        return "No se encontró una Categoria coincidente.", False
    