from typing import List, Optional
from feature.chatbot.api.category_api import get_category_api,get_categories_api
from feature.chatbot.models.category_model import CategoryModel
from difflib import get_close_matches

def get_categories_action() -> List[CategoryModel]:
    records = []
    try: 
        response = get_categories_api()
        for _ in response["items"]:
            record = CategoryModel(
                id=_["id"],
                name=_["nombre"],
                description=_["descripcion"],
                activo=_["activo"]    
            )
            records.append(record)
    except Exception as e:
        print(e)
    finally:    
        return records
    
def get_category_action(name: str) -> Optional[CategoryModel]:
    try:
        response = get_category_api()

        # Extraer los nombres de especialidades en minúsculas
        specialty_names = [item["nombre"].strip().lower() for item in response["items"]]

        # Buscar la coincidencia más cercana usando difflib
        closest_match = get_close_matches(name, specialty_names, n=1, cutoff=0.7)
        
        if closest_match:
            # Buscar el registro correspondiente a la coincidencia más cercana
            for _ in response["items"]:
                if _["nombre"].strip().lower() == closest_match[0]:
                    return {
                        "id": _["id"],
                        "name": _["nombre"],
                        "description": _["descripcion"],
                        "activo": _["activo"]
                    }

    except Exception as e:
        print(e)

    return None