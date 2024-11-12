
from feature.chatbot.action.specialty.get_specialties_action import get_specialty_action
from feature.chatbot.services.other_service import get_service_details_message
from feature.chatbot.action.view.get_service_user_view_action import get_service_user_by_specialty
from feature.chatbot.utils.json_utils import load_from_json
from feature.chatbot.view.message_state import get_messages
from feature.chatbot.models.service_user_view_model import ServiceUserViewModel
from unidecode import unidecode
import os
import re
import json
from typing import Tuple, List
from difflib import get_close_matches

def classify_servicies(id: str):
    services = get_service_user_by_specialty(id)
    if services:
        for idx, service in enumerate(services):
            get_service_details_message(service,idx)



def classify_selection_service() -> Tuple[str, bool]:
    """
    Clasifica los servicios basados en el último mensaje enviado por el usuario.

    Returns:
        Tuple[str, bool]: Mensaje de respuesta y un indicador de éxito.
    """
    try:
        specialty = load_from_json()[0]['area'].strip().lower()
        specialty_id = get_specialty_action(specialty)
        # Obtener los servicios basados en el ID de la especialidad
        print('specialty_id: ',specialty_id)
        print('specialty:',specialty)
        services = get_service_user_by_specialty(specialty_id["id"])
        
        print('services: ',services)
        
        if not services:
            return "No se encontraron servicios para la especialidad proporcionada.", False

        # Crear una lista de nombres de servicios en minúsculas
        service_names = [service.nombre_servicio.lower() for service in services]
        
        # Obtener el último mensaje enviado por el usuario y normalizarlo
        last_message = get_messages()[-1]['text'].strip().lower()
        
        # print("Servicios disponibles:", service_names)
        # print("Último mensaje:", last_message)

        # Cargar la lista de stopwords desde el archivo JSON
        stopwords = load_stopwords()
        if stopwords is None:
            return "Error al cargar las palabras vacías. Por favor, inténtalo de nuevo más tarde.", False

        # Tokenizar el último mensaje y eliminar stopwords
        words = set(re.findall(r'\w+', last_message)) - stopwords

        # Crear un diccionario de palabras clave para cada servicio
        service_keywords = {
    unidecode(service.nombre_servicio.lower()): set(unidecode(service.nombre_servicio.lower()).split()) - stopwords
    for service in services
}

        # Calcular la puntuación de coincidencia para cada servicio
        best_services = match_services_by_keywords(words, service_keywords)

        # Si se encontraron coincidencias exactas
        if best_services:
            if len(best_services) == 1:
                return best_services[0].capitalize(), True
            else:
                services_list = ', '.join([s.capitalize() for s in best_services])
                return f"He encontrado varios servicios: {services_list}. ¿Cuál te interesa?", False

        # Si no se encontraron coincidencias exactas, usar coincidencia difusa
        close_matches = get_close_matches(' '.join(words), service_names, n=1, cutoff=0.5)
        if close_matches:
            return close_matches[0].capitalize(), True

        return "No se encontró un servicio similar.", False

    except Exception as e:
        print(f"Error en classify_selection_service: {e}")
        return "Ocurrió un error al clasificar el servicio. Por favor, inténtalo de nuevo.", False


def load_stopwords() -> set:
    """
    Carga la lista de stopwords desde un archivo JSON.

    Returns:
        set: Conjunto de palabras vacías.
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        utils_dir = os.path.join(current_dir, '..', 'utils')
        stopwords_path = os.path.join(utils_dir, 'stopwords.json')

        with open(stopwords_path, 'r', encoding='utf-8') as f:
            stopwords_list = json.load(f)
        return set(stopwords_list)
    except Exception as e:
        print(f"Error al cargar stopwords: {e}")
        return None


def match_services_by_keywords(words: set, service_keywords: dict) -> List[str]:
    """
    Calcula la puntuación de coincidencia para cada servicio basado en palabras clave.

    Args:
        words (set): Palabras del mensaje del usuario.
        service_keywords (dict): Palabras clave para cada servicio.

    Returns:
        List[str]: Lista de servicios que coinciden mejor.
    """
    max_score = 0
    best_services = []

    for service_name, keywords in service_keywords.items():
        score = len(keywords & words)
        if score > max_score:
            max_score = score
            best_services = [service_name]
        elif score == max_score and score > 0:
            best_services.append(service_name)

    return best_services
