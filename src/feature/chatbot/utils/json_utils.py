import json
import os

def save_to_json(area, file_path="./conversation_log.json"):
    """Guarda el área y el servicio en un archivo JSON en el formato deseado."""
    data = []

    # Cargar datos existentes si el archivo ya existe
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)

    # Agregar la nueva entrada
    new_entry = {"area": area}
    data.append(new_entry)

    # Guardar la lista actualizada en el archivo JSON
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_from_json(file_path="./conversation_log.json"):
    """Carga las conversaciones desde un archivo JSON."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []


def clear_json(file_path="./conversation_log.json"):
    """Limpia el archivo JSON al reiniciar el bot."""
    with open(file_path, 'w') as file:
        json.dump([], file, indent=4)