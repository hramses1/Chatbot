from typing import List, Optional, Dict
from feature.chatbot.api.service_api import get_service_api,get_services_api
from feature.chatbot.models.service_model import ServiceModel

def get_services_action() -> List[ServiceModel]:
    records = []
    try:
        response = get_services_api()
        for _ in response["items"]:
            record = ServiceModel(
                id=_["id"],
                category=_["categoria"],
                name=_["nombre"],
                description=_["descripcion"],
                price=_["precio"],
                status=_["activo"],
                reference_user_id=_["usuario_referencia_id"] 
            )

            records.append(record)
    except Exception as e:
        print(e)
    finally:    
        return records

def get_service_action(id: str) -> Optional[List[Dict[str, str]]]:
    try:
        response = get_service_api()
        services = []

        # Buscar todos los registros que coinciden con la categoría
        for item in response["items"]:
            if item["categoria"] == id:
                services.append({
                    "name": item["nombre"],
                    "description": item["descripcion"],
                    "price": item["precio"],
                    "status": item["activo"],
                    "reference_user_id": item["usuario_referencia_id"]
                })

        # Retorna la lista de servicios encontrados o None si está vacía
        return services if services else None

    except Exception as e:
        print(e)
        return None