
from feature.chatbot.services.other_service import get_service_details_message
from feature.chatbot.action.view.get_service_user_view_action import get_service_user_by_specialty
from feature.chatbot.utils.json_utils import get_all_data_from_json, save_to_json
from feature.chatbot.view.message_state import get_messages
from feature.chatbot.models.service_user_view_model import ServiceUserViewModel

import os
import re
import json
from typing import Tuple, Union

def classify_servicies(id: str):
    """
    Muestra los detalles de los servicios para una especialidad dada.
    """
    services = get_service_user_by_specialty(id)
    if services:
        for idx, service in enumerate(services):
            get_service_details_message(service, idx)

def classify_selection_service() -> Tuple[Union[str, dict], bool]:
    """
    Clasifica los servicios basados en la opción seleccionada por el usuario.

    Returns:
        Tuple[Union[str, dict], bool]: Diccionario con los detalles del servicio y un indicador de éxito,
                                       o un mensaje de error si no se encontró una coincidencia.
    """
    try:
        # Obtener el último mensaje enviado por el usuario
        last_message = get_messages()[-1]['text'].strip().lower()
        data = get_all_data_from_json()
        area_id = data["area"]
        
        # Verificar que los servicios estén cargados en session_state
        print(f"Servicios: {area_id}")
        services = get_service_user_by_specialty(area_id)

        len_service = len(services)
        
        # Detectar si el usuario ingresó una opción válida
        match_option = re.search(r'opci[oó]n\s*(\d+)', last_message)
        match_number = re.fullmatch(r'\d+', last_message)
        
        if match_option:
            option_number = int(match_option.group(1))  # Captura "opción X"
        elif match_number:
            option_number = int(match_number.group(0))  # Captura un número directamente
        else:
            return "Por favor, selecciona una opción válida (por ejemplo, 'opción 1' o '1').", False

        # Verificar si la opción está dentro del rango de servicios disponibles
        if option_number < 1 or option_number > len_service :
            return f"La opción {option_number} no es válida. Por favor, selecciona una opción entre 1 y {len_service}.", False

        # Obtener el servicio seleccionado
        selected_service = services[option_number - 1]
        service_details = format_service_details(selected_service)
        
        if service_details is not None:
            # Guardar los detalles del servicio seleccionado
            save_to_json(service_details)
            return service_details, True
        else:
            return None, False
        

    except Exception as e:
        print(f"Error en classify_selection_service: {e}")
        return "Ocurrió un error al procesar tu selección. Por favor, inténtalo de nuevo.", False


def match_services_by_keywords(words: set, service_keywords: dict) -> Union[dict, None]:
    max_score = 0
    best_service = None

    for service_name, data in service_keywords.items():
        score = len(data["keywords"] & words)
        if score > max_score:
            max_score = score
            best_service = data["details"]
    
    if best_service:
        return format_service_details(best_service)
    
    return None


def format_service_details(service: ServiceUserViewModel) -> dict:
    """Formatea los detalles del servicio en un diccionario."""
    return {
        "id_servicio": service.id_servicio,
        "nombre_servicio": service.nombre_servicio,
        "nombre_usuario": service.nombre_usuario,
        'id_usuario': service.id_usuario,
        "correo_usuario": service.correo_usuario,
        "horario_fin": service.horario_fin,
        "horario_usuario": service.horario_usuario,
        "tiempo_consulta": service.tiempo_consulta,
        "descripcion_servicio": service.descripcion_servicio,
        "precio_servicio": service.precio_servicio
    }



def load_stopwords() -> set:
    """Carga la lista de stopwords desde un archivo JSON."""
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
