import json
import os

def save_to_json(data_dict, file_path="./src/feature/chatbot/utils/conversation_log.json"):
    """
    Guarda un diccionario en un archivo JSON.
    
    Parámetros:
        data_dict (dict): Diccionario con los datos a guardar (ej. {"clave": "valor"}).
        file_path (str): Ruta del archivo JSON.
    """
    # Inicializar la lista donde se guardarán los datos
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