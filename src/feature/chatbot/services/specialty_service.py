import os
import re
import json
from typing import Tuple
from feature.chatbot.action.specialty.get_specialties_action import get_specialties_action
from feature.chatbot.action.view.get_service_user_view_action import get_service_user_by_specialty
from feature.chatbot.utils.json_utils import clear_json, load_keywords

def classify_specialties(texto: str) -> Tuple[str, bool]:
    normalized_text = texto.strip().lower()
    
    # Obtener todas las especialidades desde la base de datos
    specialties = get_specialties_action()  # Devuelve una lista de SpecialtyModel

    # Verificar si el texto contiene el nombre completo de alguna especialidad
    for specialty in specialties:
        if specialty.name.lower() in normalized_text or specialty.description.lower() in normalized_text:
            services = get_service_user_by_specialty(specialty.id)
            if services:
                print(f'Se ha encontrado una coincidencia exacta, {specialty.name}')
                clear_json()
                return f"{specialty.id}", True
            else:
                None
                
    keywords = load_keywords("stopwords.json")

    # Extraer palabras clave
    stopwords = keywords.get("stopwords", [])
    
    stopwords = set(stopwords)  # Convertir stopwords a conjunto (si no lo es ya)

    words = set(re.findall(r'\w+', normalized_text)) - stopwords

    # Crear un diccionario de palabras clave para cada especialidad (nombre y descripción)
    specialty_keywords = {}
    for specialty in specialties:
        area_name = specialty.name.lower()
        description = specialty.description.lower()
        # Generar palabras clave a partir del nombre y la descripción
        keywords = set(area_name.split() + description.split()) - stopwords
        specialty_keywords[specialty.id] = {
            "keywords": keywords,
            "name": area_name,
            "description": description
        }

    # Calcular la puntuación de coincidencia para cada especialidad usando nombre y descripción
    max_score = 0
    best_specialties = []
    for specialty_id, data in specialty_keywords.items():
        score = len(data["keywords"] & words)
        if score > max_score:
            max_score = score
            best_specialties = [specialty_id]
        elif score == max_score and score > 0:
            best_specialties.append(specialty_id)

    # Si se encontró una especialidad con una puntuación máxima
    if best_specialties:
        if len(best_specialties) == 1:
            specialty = next((s for s in specialties if s.id == best_specialties[0]), None)
            if specialty:
                services = get_service_user_by_specialty(specialty.id)
                if services:
                    print(f'Se ha encontrado una coincidencia exacta, {specialty.name}')
                    clear_json()
                    return f"{specialty.id}", True
                else:
                    None
        else:
            # Si hay múltiples especialidades con la misma puntuación, proporcionar opciones
            areas_list = ', '.join([specialty_keywords[s]["name"].capitalize() for s in best_specialties])
            return f"He encontrado varias áreas que podrían interesarte: {areas_list}. ¿Podrías especificar cuál?", False

    return normalized_text, False
