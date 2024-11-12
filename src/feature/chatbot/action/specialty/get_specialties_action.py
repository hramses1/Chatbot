from typing import List, Optional
from feature.chatbot.api.specialty_api import get_specialties_api
from feature.chatbot.models.specialty_model import SpecialtyModel
from difflib import get_close_matches

def get_specialties_action() -> List[SpecialtyModel]:
    records = []
    try:
        
        response = get_specialties_api()

        for _ in response["items"]:
            record = SpecialtyModel(
                id=_["id"],
                name=_["nombre"],
                description=_["descripcion"],    
            )

            records.append(record)
    except Exception as e:
        print(e)
    finally:    
        return records

def get_specialty_action(id: str) -> Optional[SpecialtyModel]:
    try:
        response = get_specialties_api()

        # Extraer los nombres de especialidades en minúsculas
        specialty_names = [item["id"].strip().lower() for item in response["items"]]

        # Buscar la coincidencia más cercana usando difflib
        closest_match = get_close_matches(id, specialty_names, n=1, cutoff=0.7)
        
        if closest_match:
            # Buscar el registro correspondiente a la coincidencia más cercana
            for _ in response["items"]:
                if _["id"].strip().lower() == closest_match[0]:
                    return {
                        "id": _["id"],
                        "name": _["nombre"],
                        "description": _["descripcion"]
                    }

    except Exception as e:
        print(e)

    return None