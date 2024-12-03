import json
import os

def save_to_json(data_dict, file_path="./src/feature/chatbot/utils/conversation_log.json"):
    """Guarda un diccionario en un archivo JSON."""
    data = []

    # Cargar datos existentes si el archivo ya existe
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)

    # Agregar la nueva entrada al archivo JSON
    data.append(data_dict)

    # Guardar la lista actualizada en el archivo JSON
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def load_from_json(file_path="./src/feature/chatbot/utils/conversation_log.json"):
    """Carga las conversaciones desde un archivo JSON."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []


def clear_json(file_path="./src/feature/chatbot/utils/conversation_log.json"):
    """Limpia el archivo JSON al reiniciar el bot."""
    with open(file_path, 'w') as file:
        json.dump([], file, indent=4)


def get_all_data_from_json(file_path="./src/feature/chatbot/utils/conversation_log.json") -> dict:
    """
    Extrae todos los datos relevantes del archivo JSON utilizando `load_from_json`.
    
    Returns:
        dict: Diccionario con área, detalles del servicio, validez de selección, datos del usuario y tiempos de cita.
    """
    data = load_from_json(file_path)
    
    result = {
        "area": None,
        "service_details": None,
        "is_selection_valid": False,
        "user_info": None,
        "appointment_timing": None,
        "status_appointment": False,
        "state_chat": None
    }

    for entry in data:
        if "area" in entry:
            result["area"] = entry["area"]
        elif "id_servicio" in entry:
            result["service_details"] = {
                "id_servicio": entry.get("id_servicio"),
                "nombre_servicio": entry.get("nombre_servicio"),
                'precio_servicio': entry.get("precio_servicio"),
                "id_usuario": entry.get("id_usuario"),
                "nombre_usuario": entry.get("nombre_usuario"),
                "correo_usuario": entry.get("correo_usuario"),
                "horario_usuario": entry.get("horario_usuario"),
                "tiempo_consulta": entry.get("tiempo_consulta")
            }
        elif "is_selection_valid" in entry:
            result["is_selection_valid"] = entry["is_selection_valid"]
        elif "nombre" in entry and "email" in entry and "id" in entry:
            result["user_info"] = {
                "nombre": entry.get("nombre"),
                "email": entry.get("email"),
                "id": entry.get("id")
            }
        elif "Fecha y hora de inicio" in entry and "Fecha y hora de fin" in entry:
            result["appointment_timing"] = {
                "start_time": entry.get("Fecha y hora de inicio"),
                "end_time": entry.get("Fecha y hora de fin")
            }
        elif 'status_appointment' in entry:
            result['status_appointment'] = entry['status_appointment']
        
        elif 'state_chat' in entry:
            result['state_chat'] = entry['state_chat']

    return result


def load_keywords(file_path: str) -> dict:
    """Cargar palabras clave desde un archivo JSON."""
    
     # Construir la ruta al archivo stopwords.json en utils
     
    current_dir = os.path.dirname(os.path.abspath(__file__))
    utils_dir = os.path.join(current_dir, '..', 'utils')
    stopwords_path = os.path.join(utils_dir, file_path)
    
    with open(stopwords_path, 'r', encoding='utf-8') as file:
        stopwords_list =json.load(file)
        return stopwords_list
