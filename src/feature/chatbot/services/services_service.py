from feature.chatbot.services.other_service import get_service_details_message
from feature.chatbot.action.category.get_category_action import get_category_action
from feature.chatbot.view.message_state import initialize_messages, get_messages, add_message 
from feature.chatbot.utils.json_utils import load_from_json
import os
import re
import json
from typing import Tuple
from difflib import get_close_matches
from feature.chatbot.action.service.get_services_action import get_service_action, get_services_action


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



def classify_selection_service() -> Tuple[str, bool]:
    # Obtener el área desde un archivo JSON
    close_match = load_from_json()[0]['area'].strip().lower()
    
    print(f"Área seleccionada: {close_match}")
    normalized_name_area_selected = f"servicios de derecho {close_match}"
    
    # Obtener la categoría basada en el área seleccionada
    category = get_category_action(normalized_name_area_selected)
    if not category:
        return "No se encontró una Categoria coincidente.", False
    
    # Obtener la lista de servicios de la categoría encontrada
    services = get_service_action(category["id"])
    if not services:
        return "No se encontraron servicios disponibles.", False

    # Crear una lista de nombres de servicios en minúsculas
    service_names = [service['name'].lower() for service in services if 'name' in service]
    
    # Obtener el último mensaje enviado y normalizarlo
    last_message = get_messages()[-1]['text'].strip().lower()
    
    print("Servicios disponibles:", service_names)
    print("Último mensaje:", last_message)

    # Construir la ruta al archivo stopwords.json en utils
    current_dir = os.path.dirname(os.path.abspath(__file__))
    utils_dir = os.path.join(current_dir, '..', 'utils')
    stopwords_path = os.path.join(utils_dir, 'stopwords.json')

    # Cargar la lista de stopwords desde el archivo JSON
    try:
        with open(stopwords_path, 'r', encoding='utf-8') as f:
            stopwords_list = json.load(f)
            stopwords = set(stopwords_list)
    except Exception as e:
        return "Error al cargar las palabras vacías. Por favor, inténtalo de nuevo más tarde.", False

    # Tokenizar el último mensaje y eliminar stopwords
    words = set(re.findall(r'\w+', last_message)) - stopwords

    # Crear un diccionario de palabras clave para cada servicio
    service_keywords = {}
    for service in services:
        service_name = service['name'].lower()
        # Generar palabras clave a partir del nombre del servicio
        keywords = set(service_name.split()) - stopwords
        service_keywords[service_name] = keywords

    # Calcular la puntuación de coincidencia para cada servicio
    max_score = 0
    best_services = []
    for service_name, keywords in service_keywords.items():
        score = len(keywords & words)
        if score > max_score:
            max_score = score
            best_services = [service_name]
        elif score == max_score and score > 0:
            best_services.append(service_name)

    # Si se encontraron servicios con la mejor coincidencia
    if best_services:
        if len(best_services) == 1:
            return best_services[0].capitalize(), True
        else:
            services_list = ', '.join([s.capitalize() for s in best_services])
            return f"He encontrado varios servicios: {services_list}. ¿Cuál te interesa?", False

    # Si no se encontraron coincidencias, usar coincidencia difusa
    close_matches = get_close_matches(' '.join(words), service_names, n=1, cutoff=0.5)
    if close_matches:
        match_name = close_matches[0]
        return match_name.capitalize(), True

    return "No se encontró un mensaje similar.", False
