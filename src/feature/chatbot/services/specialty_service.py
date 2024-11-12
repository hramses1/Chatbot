import os
import re
import json
from typing import Tuple
from difflib import get_close_matches
from feature.chatbot.action.specialty.get_specialties_action import get_specialties_action
from feature.chatbot.utils.json_utils import clear_json

def classify_specialties(texto: str) -> Tuple[str, bool]:
    normalized_text = texto.strip().lower()
    # Obtener todas las especialidades desde la base de datos
    specialties = get_specialties_action()  # Devuelve una lista de SpecialtyModel

    # Crear una lista de nombres de especialidades en minúsculas
    specialty_names = [specialty.name.lower() for specialty in specialties]

    # Verificar si el texto contiene el nombre completo de alguna especialidad
    for specialty_name in specialty_names:
        if specialty_name in normalized_text:
            # Devolver la especialidad correspondiente
            specialty = next((s for s in specialties if s.name.lower() == specialty_name), None)
            if specialty:
                print('Primero')
                clear_json()
                return f"{specialty.id}", True

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
        # Manejar errores en la carga del archivo
        return "Error al cargar las palabras vacías. Por favor, inténtalo de nuevo más tarde.", False

    # Tokenizar el texto y eliminar stopwords
    words = set(re.findall(r'\w+', normalized_text)) - stopwords

    # Crear un diccionario de palabras clave para cada especialidad
    specialty_keywords = {}
    for specialty in specialties:
        area_name = specialty.name.lower()
        # Generar palabras clave a partir del nombre de la especialidad
        keywords = set(area_name.split()) - stopwords
        specialty_keywords[area_name] = keywords

    # Calcular la puntuación de coincidencia para cada especialidad
    max_score = 0
    best_specialties = []
    for area_name, keywords in specialty_keywords.items():
        score = len(keywords & words)
        if score > max_score:
            max_score = score
            best_specialties = [area_name]
        elif score == max_score and score > 0:
            best_specialties.append(area_name)

    if best_specialties:
        if len(best_specialties) == 1:
            specialty_name = best_specialties[0]
            specialty = next((s for s in specialties if s.name.lower() == specialty_name), None)
            if specialty:
                print('Segundo')
                clear_json()
                return f"{specialty.id}", True
        else:
            areas_list = ', '.join([s.capitalize() for s in best_specialties])
            return f"He encontrado varias áreas: {areas_list}. ¿Cuál te interesa?", False
        
    return normalized_text, False
